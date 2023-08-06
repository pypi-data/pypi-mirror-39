#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Ingest module."""
from sys import argv as sys_argv
from time import sleep
from threading import Thread
from argparse import ArgumentParser, SUPPRESS
import cherrypy
from pacifica.ingest.rest import Root, error_page_default
from pacifica.ingest.orm import database_setup, update_state
from pacifica.ingest.globals import CHERRYPY_CONFIG


def stop_later(doit=False):
    """Used for unit testing stop after 60 seconds."""
    if not doit:  # pragma: no cover
        return

    def sleep_then_exit():
        """
        Sleep for 60 seconds then call cherrypy exit.

        Hopefully this is long enough for the end-to-end tests to finish
        """
        sleep(90)
        cherrypy.engine.exit()
    sleep_thread = Thread(target=sleep_then_exit)
    sleep_thread.daemon = True
    sleep_thread.start()


def main(argv=None):
    """Main method to start the httpd server."""
    parser = ArgumentParser(description='Run the cart server.')
    parser.add_argument('-c', '--config', metavar='CONFIG', type=str,
                        default=CHERRYPY_CONFIG, dest='config',
                        help='cherrypy config file')
    parser.add_argument('-p', '--port', metavar='PORT', type=int,
                        default=8066, dest='port',
                        help='port to listen on')
    parser.add_argument('-a', '--address', metavar='ADDRESS',
                        default='localhost', dest='address',
                        help='address to listen on')
    parser.add_argument('--stop-after-a-moment', help=SUPPRESS,
                        default=False, dest='stop_later',
                        action='store_true')
    args = parser.parse_args(argv)
    database_setup()
    stop_later(args.stop_later)
    cherrypy.config.update({'error_page.default': error_page_default})
    cherrypy.config.update({
        'server.socket_host': args.address,
        'server.socket_port': args.port
    })
    cherrypy.quickstart(Root(), '/', args.config)


def cmd(argv=None):
    """Command line admin tool for managing ingest."""
    parser = ArgumentParser(description='Admin command line tool.')
    subparsers = parser.add_subparsers(help='sub-command help')
    job_parser = subparsers.add_parser(
        'job', help='job help', description='manage jobs')
    for attr in ['job_id', 'state', 'task', 'task_percent', 'exception']:
        job_parser.add_argument(
            '--{}'.format(attr.replace('_', '-')),
            dest=attr,
            help='set the {}'.format(attr)
        )
    job_parser.set_defaults(func=update_state)
    args = parser.parse_args(argv)
    args_func = args.func
    delattr(args, 'func')
    args_func(**(vars(args)))


if __name__ == '__main__':
    main(sys_argv[1:])
