#!/usr/bin/env bash

PORT="${PORT:-7080}"
export FLASK_APP=tread
export FLASK_ENV=development
flask run --port $PORT --host 0.0.0.0 --debug
