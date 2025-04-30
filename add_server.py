#!/usr/bin/env python3
import cgi
import sqlite3
import sys

# Parse form data
form = cgi.FieldStorage()
name = form.getfirst('name', '').strip()
ip   = form.getfirst('ip', '').strip()

# Insert into the database if both fields are present
if name and ip:
    conn = sqlite3.connect('data/servers.db')
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO servers (name, ip) VALUES (?, ?)",
        (name, ip)
    )
    conn.commit()
    conn.close()

# Redirect back to the list
print("Status: 303 See Other")
print("Location: /list_servers.py")
print()  # End of headers
