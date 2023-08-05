#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test ingest."""
import mock
import peewee
from pacifica.ingest.orm import database_setup, IngestState


@mock.patch.object(IngestState, 'table_exists')
def test_bad_db_connection(mock_is_table_exists):
    """Test a failed db connection."""
    mock_is_table_exists.side_effect = peewee.OperationalError(
        mock.Mock(), 'Error')
    hit_exception = False
    try:
        database_setup(18)
    except peewee.OperationalError:
        hit_exception = True
    assert hit_exception
