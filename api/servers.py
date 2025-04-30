#!/usr/bin/env python3
import os
import json
import sqlite3
import sys

# Determine absolute path to the SQLite DB
script_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(script_dir, '..', 'data', 'servers.db')

# Parse PATH_INFO for optional ID (e.g. /api/servers.py/3)
path = os.environ.get('PATH_INFO', '').lstrip('/')
parts = path.split('/') if path else []

# Connect to the database
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Helper to emit JSON response
def respond(status_code, payload):
    print(f"Status: {status_code}")
    print("Content-Type: application/json")
    print()
    print(json.dumps(payload))
    sys.exit(0)

try:
    if parts and parts[0]:
        # Detail endpoint: /api/servers.py/<ID>
        try:
            server_id = int(parts[0])
        except ValueError:
            respond(400, {"error": "Invalid server ID"})
        cur.execute(
            """
            SELECT
              id,
              owner,
              description,
              CASE WHEN ready=1 THEN instance_id ELSE NULL END AS instance_id,
              CASE WHEN ready=1 THEN instance_id ELSE NULL END AS ip_if_ready,
              ready
            FROM servers
            WHERE id = ?
            """,
            (server_id,)
        )
        row = cur.fetchone()
        if not row:
            respond(404, {"error": "Server not found"})
        respond(200, dict(row))
    else:
        # List endpoint: /api/servers.py
        cur.execute(
            """
            SELECT
              id,
              owner,
              description,
              CASE WHEN ready=1 THEN instance_id ELSE NULL END AS instance_id,
              CASE WHEN ready=1 THEN instance_id ELSE NULL END AS ip_if_ready,
              ready
            FROM servers
            """
        )
        rows = cur.fetchall()
        respond(200, [dict(r) for r in rows])
finally:
    conn.close()
