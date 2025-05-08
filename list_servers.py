#!/usr/bin/env python3
import os, sqlite3, sys

# 1) Read session cookie
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

# 2) Lookup username
db_path = os.path.join(os.path.dirname(__file__), "data", "servers.db")
conn = sqlite3.connect(db_path)
cur  = conn.cursor()
cur.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
row = cur.fetchone()
if not row:
    # invalid session → back to login
    print("Status: 303 See Other")
    print("Location: /login.html\n")
    sys.exit(0)
username = row[0]

# 3) Render HTML list filtered by owner=username
print("Content-Type: text/html\n")
print("<!DOCTYPE html><html><head><meta charset='utf-8'><title>Server List</title></head><body>")
print(f"<h1>{username}’s Servers</h1>")
print("<ul>")

cur.execute("""
  SELECT id,
         CASE WHEN ready=1 THEN instance_id ELSE 'pending' END AS ip
  FROM servers
  WHERE owner = ?
""", (username,))

for sid, ip in cur.fetchall():
    print(f"""<li>{ip} 
      <a href="/terminate_server.py?id={sid}">[Terminate]</a>
    </li>""")

conn.close()

print("</ul>")
print("<p><a href=\"/index.py\">Back to Dashboard</a></p>")
print("</body></html>")
