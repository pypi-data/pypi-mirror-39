#!/bin/bash
pylint --rcfile=pylintrc IngestServer.py DatabaseCreate.py ingest setup.py
radon cc *.py ingest
