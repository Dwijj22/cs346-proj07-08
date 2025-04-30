#!/usr/bin/env python3
import sqlite3

# HTTP header
print("Content-Type: text/html")
print()

# Connect to the mounted SQLite database
conn = sqlite3.connect('data/servers.db')
cur  = conn.cursor()
cur.execute("SELECT name, ip FROM servers;")
rows = cur.fetchall()
conn.close()

# Generate HTML
print("<!DOCTYPE html>")
print("<html><head><meta charset='utf-8'><title>Server List</title></head><body>")
print("<h1>Server List</h1><ul>")
for name, ip in rows:
    print(f"<li>{name} – {ip}</li>")
print("</ul></body></html>")
