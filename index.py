#!/usr/bin/env python3
import os, sqlite3, sys

# 1) Session check (same as list_servers.py)
cookie = os.environ.get('HTTP_COOKIE','')
session_id = None
for part in cookie.split(';'):
    if part.strip().startswith('session='):
        session_id = part.split('=',1)[1]
        break
if not session_id:
    print("Status: 303 See Other")
    print("Location: /login.html\n")
    sys.exit(0)

db_path = os.path.join(os.path.dirname(__file__), 'data', 'servers.db')
conn = sqlite3.connect(db_path)
cur  = conn.cursor()
cur.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
row = cur.fetchone()
conn.close()
if not row:
    print("Status: 303 See Other")
    print("Location: /login.html\n")
    sys.exit(0)
username = row[0]

# 2) Render dashboard with embedded form
print("Content-Type: text/html\n")
print(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Dashboard</title></head><body>
  <h1>Welcome, {username}</h1>
  <h2>Add a New Server</h2>
  <form method="GET" action="/create_server.py">
    Description: <input name="desc" required>
    <button type="submit">Add Server</button>
  </form>
  <ul>
    <li><a href="/list_servers.py">View My Servers</a></li>
    <li><a href="/api/servers.py">List Servers (JSON)</a></li>
    <li><a href="/logout.py">Log Out</a></li>
  </ul>
</body></html>""")
