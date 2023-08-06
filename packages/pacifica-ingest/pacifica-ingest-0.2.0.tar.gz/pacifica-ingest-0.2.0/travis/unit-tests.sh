#!/bin/bash
export POLICY_PID=$(cat travis/policy/PolicyServer.pid)
export ARCHIVE_INTERFACE_PID=$(cat travis/archivei/archiveinterface.pid)
export MYSQL_ENV_MYSQL_USER=travis
export MYSQL_ENV_MYSQL_PASSWORD=
export BROKER_TRANSPORT=redis
export BROKER_PORT=6379
export BROKER_USER=
export BROKER_PASS=
echo foo > /tmp/foo.txt
coverage run --include='ingest*' -p -m celery -A ingest.backend worker --loglevel=info -c 1 -P solo &
CELERY_PID=$!
coverage run --include='ingest*' -p IngestServer.py --stop-after-a-moment &
SERVER_PID=$!
coverage run --include='ingest*' -m -p pytest -v ingest/test/test_ingest.py ingest/test/test_upload.py ingest/test/test_utils.py ingest/test/test_move.py
kill $POLICY_PID
coverage run --include='ingest*' -m -p pytest -v ingest/test/test_upload_badpolicy.py
pushd travis/policy
PolicyServer.py &
echo $! > PolicyServer.pid
popd
export POLICY_PID=$(cat travis/policy/PolicyServer.pid)
kill $ARCHIVE_INTERFACE_PID
sleep 2
coverage run --include='ingest*' -m -p pytest -v ingest/test/test_upload_badai.py
kill $CELERY_PID $POLICY_PID
wait
# can run the server straight from module
coverage run --include='ingest*' -p -m ingest --stop-after-a-moment
kill -9 $SERVER_PID $CELERY_PID || true
wait
coverage run --include='ingest*' -m -p pytest -v ingest/test/test_entry_points.py
coverage combine -a .coverage*
coverage report --show-missing --fail-under=100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
