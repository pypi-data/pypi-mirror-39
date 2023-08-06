#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from os import getenv
try:
    from ConfigParser import SafeConfigParser
except ImportError:  # pragma: no cover python 2 vs 3 issue
    from configparser import SafeConfigParser
from pacifica.ingest.globals import CONFIG_FILE


def get_config():
    """Return the ConfigParser object with defaults set."""
    configparser = SafeConfigParser()
    configparser.add_section('database')
    configparser.set('database', 'peewee_url', getenv(
        'PEEWEE_URL', 'sqliteext:///db.sqlite3'))
    configparser.add_section('celery')
    configparser.set('celery', 'broker_url', getenv(
        'BROKER_URL', 'pyamqp://'))
    configparser.set('celery', 'backend_url', getenv(
        'BACKEND_URL', 'rpc://'))
    configparser.read(CONFIG_FILE)
    return configparser
