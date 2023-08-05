#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Testable utilities for ingest."""
from __future__ import print_function
import os
import json
import requests


def create_state_response(record):
    """Create the state response body from a record."""
    return {
        'job_id': record.job_id,
        'state': record.state,
        'task': record.task,
        'task_percent': str(record.task_percent),
        'updated': str(record.updated),
        'created': str(record.created),
        'exception': str(record.exception)
    }


def get_unique_id(id_range, mode):
    """Return a unique job id from the id server."""
    uniqueid_server = os.getenv('UNIQUEID_SERVER', '127.0.0.1')
    uniqueid_port = os.getenv('UNIQUEID_PORT', '8051')

    url = 'http://{0}:{1}/getid?range={2}&mode={3}'.format(
        uniqueid_server, uniqueid_port, id_range, mode)

    req = requests.get(url)
    body = req.text
    info = json.loads(body)
    unique_id = info['startIndex']

    return unique_id
