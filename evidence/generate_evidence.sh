#!/usr/bin/env bash
# Generates the REAL text evidence files for the capstone tasks by running the app and calling its API.
#
#   bash evidence/generate_evidence.sh                      # starts a local server on :8000, records everything
#   BASE_URL=https://your-app.onrender.com bash evidence/generate_evidence.sh   # test a deployed site instead
#
# Requires: python3 with `pip install -r requirements.txt` done, and curl.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
PY="${PYTHON:-python3}"; command -v "$PY" >/dev/null 2>&1 || PY=python
PORT="${PORT:-8000}"
DEMO_USER="${DEMO_USER:-demo}"
DEMO_PASS="${DEMO_PASS:-Demo@12345}"
export PYTHONUNBUFFERED=1
SERVER_PID=""

if [ -z "${BASE_URL:-}" ]; then
  BASE_URL="http://127.0.0.1:$PORT"
  cd "$ROOT/server" || exit 1
  "$PY" manage.py makemigrations djangoapp --noinput >/dev/null 2>&1
  "$PY" manage.py migrate --noinput >/dev/null 2>&1 || { echo "migrate failed - did you run: pip install -r requirements.txt ?"; exit 1; }
  "$PY" manage.py seed >/dev/null
  # Task 2: the server's own terminal output
  "$PY" manage.py runserver "127.0.0.1:$PORT" --noreload > "$HERE/django_server" 2>&1 &
  SERVER_PID=$!
  trap '[ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null' EXIT
fi

for _ in $(seq 1 40); do curl -sf "$BASE_URL/djangoapp/get_dealers" >/dev/null && break; sleep 0.5; done
curl -sf "$BASE_URL/djangoapp/get_dealers" >/dev/null || { echo "Server not reachable at $BASE_URL"; exit 1; }

cd "$HERE" || exit 1
rm -f cookies.txt

capture() {  # capture <output-file> <command string>
  local file="$1" cmd="$2"
  { echo "\$ $cmd"; eval "$cmd"; echo; } > "$file" 2>&1
  echo "wrote evidence/$file"
}

capture loginuser "curl -s -c cookies.txt -X POST -H 'Content-Type: application/json' -d '{\"userName\":\"$DEMO_USER\",\"password\":\"$DEMO_PASS\"}' $BASE_URL/djangoapp/login"
capture logoutuser "curl -s -b cookies.txt $BASE_URL/djangoapp/logout"
capture getdealerreviews "curl -s $BASE_URL/djangoapp/reviews/dealer/1"
capture getalldealers "curl -s $BASE_URL/djangoapp/get_dealers"
capture getdealerbyid "curl -s $BASE_URL/djangoapp/dealer/1"
capture getdealersbyState "curl -s $BASE_URL/djangoapp/get_dealers/Kansas"
capture getallcarmakes "curl -s $BASE_URL/djangoapp/get_cars"
capture analyzereview "curl -s $BASE_URL/djangoapp/analyze/Fantastic%20services"

rm -f cookies.txt
if [ -n "$SERVER_PID" ]; then sleep 1; kill "$SERVER_PID" 2>/dev/null; SERVER_PID=""; echo "wrote evidence/django_server"; fi
echo
echo "Done. Still to do by hand: screenshots (see screenshots/README.md), CICD, deploymentURL."
