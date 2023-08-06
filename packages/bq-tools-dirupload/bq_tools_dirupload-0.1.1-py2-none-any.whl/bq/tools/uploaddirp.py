#!/usr/bin/env python

from __future__ import print_function
from builtins import input
from builtins import range
import os
import sys
import re
import fnmatch
import argparse
import logging
import random
import string
import urllib3
from future import standard_library
standard_library.install_aliases()
from itertools import zip_longest

import configparser

import bqapi
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from .pool import ProcessManager

def bisque_session(args):
    "Get a bisque session"
    user = None
    password = None
    root = None
    if args.bisque_host:
        root = args.bisque_host
    if args.credentials:
        user,password = args.credentials.split(':')
    elif os.path.exists (os.path.expanduser(args.config)):
        parser = configparser.ConfigParser ()
        parser.read (os.path.expanduser(args.config))
        if root is None:
            root = parser.get (args.profile, 'host')
        user = parser.get (args.profile, 'user')
        password = parser.get (args.profile, 'password')
    if not (root and user and password):
        config = configparser.RawConfigParser()
        print ("Please configure how to connect to bisque")
        root = input ("BisQue URL e.g. https://data.viqi.org/:")
        user = input ("username:")
        password = input ("password:")
        config_file = os.path.expanduser (args.config)
        os.makedirs(os.path.dirname(config_file))
        with open (config_file, 'wb') as conf:
            config.add_section (args.profile)
            config.set(args.profile, 'host', root)
            config.set(args.profile, 'user', user)
            config.set(args.profile, 'password', password)
            config.write (conf)
            print ("configuration has been saved to", args.config)

    if root and user and password:
        session =   bqapi.BQSession()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.c.verify = False
        session = session.init_local(bisque_root=root,  user = user, pwd=password, create_mex=False)
        return session
    print ("Could not create bisque session with root={} user={} pass={}".format(root, user, password))
    return None

def send_image_to_bisque(session, args, image_path):
    "Send one image to bisque"

    # Strip off top level dirs .. except user given root
    filename = os.path.basename (image_path)
    original_image_path = image_path
    image_path = image_path[len(os.path.dirname(args.directory))+1:]

    ################
    # Skip pre-existing resources with same filename
    if args.skip:
        data_service   = session.service('data_service')
        response = data_service.get(params={ 'name': filename }, render='xml')
        if len(response) and  response[0].get ('name') == filename:
            args.log.info ("skipping %s", filename)
            return None
    ###################
    # build argument tags into upload xml
    tags  = etree.Element ('image', name=image_path)
    # add any fixed arguments
    for tag,value in [ x.split(':') for x in args.tag ]:
            etree.SubElement (tags, 'tag', name=tag, value = value)
    # path elements can be made tags
    if args.path_tags:
        for tag,value in zip_longest (args.path_tags, image_path.split ('/')):
            if tag  and value :
                etree.SubElement (tags, 'tag', name=tag, value = value)
    # RE over the filename
    if args.re_tags:
        matches = args.re_tags.match (filename)
        if matches:
            for tag, value in matches.groupdict().items():
                if tag  and value :
                    etree.SubElement (tags, 'tag', name=tag, value = value)
        else:
            args.log.warn ("RE did not match %s", filename)
    xml = etree.tostring(tags)

    ################
    # Prepare to upload
    if args.debug:
        args.log.debug ("upload %s with xml %s ", image_path, xml)
    if not args.dry_run :
        import_service = session.service('import')
        with open (original_image_path, 'rb') as fileobj:
            response = import_service.transfer(image_path, fileobj = fileobj, xml = xml, render='xml')
        return response

    # Return a dry_run response
    resource = etree.Element ('resource')
    etree.SubElement (resource, 'image', name=image_path,
                      resource_uniq = '00-%s' % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)),
                      value = image_path)
    return resource


SUCCESS=[]
ERROR = []
SKIPPED = []
UNIQS = []

def append_result_list (request):
    SUCCESS.append (request)
    resource = request['return_value']
    UNIQS.append (resource[0].get ('resource_uniq'))


def append_error_list (request):
    if request.get ('return_value') is None:
        SKIPPED.append (request)
        return
    ERROR.append (request)
    args = request['args'][1]
    if request.get ('return_value'):
        args.log.error ("return value %s", etree.tostring (request['return_value']))

DEFAULT_CONFIG='~/bisque/config' if os.name == 'nt' else "~/.bisque/config"

def main():
    parser = argparse.ArgumentParser("Upload files to bisque", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--config', help='bisque config', default=DEFAULT_CONFIG)
    parser.add_argument('--profile', help="Profile to use in bisque config", default='default')
    parser.add_argument('-n', '--dry-run', action="store_true", help='report actions w/o changes', default=False)
    parser.add_argument('-d', '--debug', action="store_true", help='print activities', default=False)
    parser.add_argument('-a', '--credentials', help= "A bisque login.. admin ", default=None)
    #parser.add_argument('-r', '--recursive', help= "descend tree of files  ", action="store_true", default=False)
    parser.add_argument('--bisque-host', help = "Default bisque server to connect to ")

    parser.add_argument('--tag', help="fixed name:value pair. Any number allow", action="append", default=[])
    parser.add_argument('--path-tags', help='tag names for a parsible path i.e. /project/date/subject/', default="")
    parser.add_argument('--re-tags', help=r're expressions for tags i.e. (?P<location>\w+)--(?P<date>[\d-]+)')
    parser.add_argument('--include', help='re expression for files to include', default=None)
    parser.add_argument('--exclude', help='re expression for files to exclude', default=None)
    parser.add_argument('--dataset', help='create dataset and add files to it', default=None)
    parser.add_argument('--threads', help='set number of uploader threads', default=8)
    parser.add_argument("-s", '--skip', help="Skip upload if there is file with the same name already present on the server", action='store_true')
    parser.add_argument('directories', help='director(ies) to upload', nargs='+' )

    args = parser.parse_args()

    #if args.debug:
    #    logging.getLogger().setLevel (logging.DEBUG)

    args.path_tags = args.path_tags.split ('/')
    args.log = logging.getLogger("bq.uploader")
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)
        args.log.debug (args)

    if args.re_tags:
        args.re_tags = re.compile (args.re_tags)

    session = bisque_session(args)
    if session is None:
        print("Failed to create session.. check credentials")
        sys.exit(1)

    # Start workers with default arguments
    manager = ProcessManager(limit=args.threads, workfun = send_image_to_bisque,
                              is_success = lambda r: r is not None and r[0].get ('name'),
                              on_success = append_result_list,
                              on_fail    = append_error_list)
    # Add files to work queue
    for directory in args.directories:
        args.directory = os.path.abspath(os.path.expanduser (directory))
        for root, dirs, files in os.walk (directory):
            for f1 in files:
                #print (root, dirs, files)
                if args.include and not fnmatch.fnmatch (f1, args.include):
                    continue
                if args.exclude and fnmatch.fnmatch (f1, args.exclude):
                    continue
                manager.schedule ( args = (session, args, os.path.join (root, f1)))

    # wait for all workers to stop
    manager.stop()
    # Store output dataset
    if args.dataset and UNIQS:
        datasets = session.service('dataset_service')
        if args.debug:
            args.log.debug ('create dataset %s with %s', args.dataset, UNIQS)
        if not args.dry_run:
            dataset = datasets.create (args.dataset, UNIQS)
            if args.debug:
                args.log.debug ('created dataset %s', etree.tostring(dataset) )
    if args.debug:
        for S in SUCCESS:
            args.log.debug ('success %s', S)
        for E in ERROR:
            args.log.debug ('failed %s', E)

    print ("Successful uploads: ", len (SUCCESS))
    print ("Failed uploads:", len (ERROR))
    print ("Skipped uploads:", len (SKIPPED))

if __name__ == "__main__":
    main()
