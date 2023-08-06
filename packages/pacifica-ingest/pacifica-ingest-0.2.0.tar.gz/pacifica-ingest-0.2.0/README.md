# Pacifica Ingest Services

[![Build Status](https://travis-ci.org/pacifica/pacifica-ingest.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-ingest)
[![Build status](https://ci.appveyor.com/api/projects/status/dhniln12ili29kgm?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-ingest)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)

[![Frontend Stars](https://img.shields.io/docker/stars/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Stars](https://img.shields.io/docker/stars/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/builds)
[![Backend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/builds)

This is the Pacifica Ingest Services API.

This service receives, validates and processes data that is provided by a
Pacifica Uploader service.

## Installing the Service

### Prerequisites

To run the code, the following commands are required:

* [Docker Compose](https://github.com/docker/compose) (the `docker-compose`
  command)

### The Manual Way

Install the dependencies using the `pip` command:

```bash
pip install -r requirements.txt
```

Build and install the code using the `setup.py` script:

```bash
python setup.py build
python setup.py install
```

## Running the Service

Start and run a new instance using the `docker-compose` command:

```bash
docker-compose up
```

## Bundle Format

The bundle format is parsed using the [tarfile](https://docs.python.org/2/library/tarfile.html)
package from the Python standard library.

Both data and metadata are stored in a bundle. Metadata is stored in the
`metadata.txt` file (JSON format). Data is stored in the `data/` directory.

To display the contents of a bundle using the `tar` command:
```bash
tar -tf mybundle.tar
```

For example, the contents of `mybundle.tar` is:
```
data/mywork/project/proposal.doc
data/mywork/experiment/results.csv
data/mywork/experiment/results.doc
metadata.txt
```

# API Examples

The endpoints that define the ingest process are as follows. The assumption is that the installer
knows the IP address and port the WSGI service is listening on.

## Ingest (Single HTTP Request)

Post a bundle ([defined above](#bundle-format)) to the endpoint.

```
POST /ingest
... tar bundle as body ...
```

The response will be the job ID information as if you requested it directly.

```json
{
  "job_id": 1234,
  "state": "OK",
  "task": "UPLOADING",
  "task_percent": "0.0",
  "updated": "2018-01-25 16:54:50",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

Failures that exist with this endpoint are during the course of uploading the bundle.
Sending data to this endpoint should consider long drawn out HTTP posts that maybe
longer than clients are used to handling.

## Move (Single HTTP Request)

Post a [metadata document](test_data/move-md.json) to the endpoint.

```
POST /move
... content of move-md.json ...
```

The response will be the job ID information as if you requested it directly.

```json
{
  "job_id": 1234,
  "state": "OK",
  "task": "UPLOADING",
  "task_percent": "0.0",
  "updated": "2018-01-25 16:54:50",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

## Get State for Job

Using the `job_id` field from the HTTP response from an ingest.

```json
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "OK",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:00:32",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

As the bundle of data is being processed errors may occure, if that happens the following
will be returned. It is useful when consuming this endpoint to plan for failures. Consider
logging or showing a message visable to the user that shows the ingest failed.

```json
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "FAILED",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:01:02",
  "created": "2018-01-25 16:54:50",
  "exception": "... some crazy python back trace ..."
}
```

# CLI Tools

There is an admin tool that consists of subcommands for manipulating ingest processes.

## Job Subcommand

The job subcommand allows administrators to directly manipulate the state of a job. Due
to complex computing environments some jobs may get "stuck" and get to a state where
they aren't failed and aren't progressing. This may happen for any number of reasons but
the solution is to manually fail the job.

```sh
IngestCMD job \
    --job-id 1234 \
    --state FAILED \
    --task 'ingest files' \
    --task-percent 0.0 \
    --exception 'Failed by adminstrator'
```

## Contributions

Contributions are accepted on GitHub via the fork and pull request workflow.
GitHub has a good [help article](https://help.github.com/articles/using-pull-requests/)
if you are unfamiliar with this method of contributing.
