#!/bin/sh
set -eu

mkdir -p /app/data

exec uv run --no-sync python -m app.main

