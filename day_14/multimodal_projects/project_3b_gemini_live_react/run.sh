#!/usr/bin/env bash
# One command: build the React app if it needs building, then serve it.
#   ./run.sh              -> http://127.0.0.1:8000
#   PORT=8010 ./run.sh    -> use a different port
set -e
cd "$(dirname "$0")"
PORT="${PORT:-8000}"

# A server left running from last time is the most common way this fails, so deal
# with it plainly: reuse OUR port if the old process is this same server, and get
# out of the way if the port belongs to something else entirely.
if holder=$(lsof -nP -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null); then
  if ps -p "$holder" -o command= | grep -q "server.py"; then
    echo "[3b] port $PORT still held by an older copy of this server (pid $holder) - stopping it"
    kill "$holder" 2>/dev/null || true
    sleep 1
  else
    echo "[3b] port $PORT is in use by something else:"
    ps -p "$holder" -o pid=,command=
    echo "[3b] run it elsewhere instead:   PORT=8010 ./run.sh"
    exit 1
  fi
fi

[ -d web/node_modules ] || (cd web && npm install)
[ -d web/dist ] || (cd web && npm run build)
exec uv run python server.py
