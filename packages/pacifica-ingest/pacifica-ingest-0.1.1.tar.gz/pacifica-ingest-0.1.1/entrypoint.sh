#!/bin/bash
if [[ -z $PEEWEE_DATABASE_URL ]] ; then
  if [[ $PEEWEE_USER && $PEEWEE_PASS ]]; then
    PEEWEE_USER_PART="${PEEWEE_USER}:${PEEWEE_PASS}@"
  fi
  if [[ $PEEWEE_PORT ]] ; then
    PEEWEE_ADDR_PART="${PEEWEE_ADDR}:${PEEWEE_PORT}"
  else
    PEEWEE_ADDR_PART=$PEEWEE_ADDR
  fi
  PEEWEE_DATABASE_URL="${PEEWEE_PROTO}://${PEEWEE_USER_PART}${PEEWEE_ADDR_PART}/${PEEWEE_DATABASE}"
fi
mkdir ~/.pacifica-ingest/
printf '[database]\npeewee_url = '${PEEWEE_DATABASE_URL}'\n' > ~/.pacifica-ingest/config.ini
python -c 'from pacifica.ingest.orm import database_setup; database_setup()'
uwsgi \
  --http-socket 0.0.0.0:8066 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/pacifica/ingest/wsgi.py "$@"
