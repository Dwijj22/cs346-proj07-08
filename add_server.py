#!/usr/bin/env python3
import cgi
import sqlite3
import os

# 1) Read form fields “name” → owner, “ip” → instance_id
form  = cgi.FieldStorage()
owner = form.getfirst('name', '').strip()
inst  = form.getfirst('ip',   '').strip()

# 2) If both were supplied, insert into servers(owner,description,instance_id,ready)
if owner and inst:
    # Build the path to your SQLite file
    here    = os.path.dirname(__file__)
    db_path = os.path.join(here, 'data', 'servers.db')

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO servers (owner, description, instance_id, ready) VALUES (?, ?, ?, 1)",
        (owner, '', inst)
    )
    conn.commit()
    conn.close()

# 3) Redirect back to the list page
print("Status: 303 See Other")
print("Location: /list_servers.py")
print()   # end of headers
