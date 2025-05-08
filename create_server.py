#!/usr/bin/env python3
import cgi, os, sqlite3, sys, time, uuid

# 1) Read session cookie
cookie = os.environ.get('HTTP_COOKIE','')
session_id = None
for part in cookie.split(';'):
    if part.strip().startswith('session='):
        session_id = part.split('=',1)[1]
        break
if not session_id:
    print("Status: 400 Bad Request\nContent-Type: text/plain\n\nNot logged in")
    sys.exit(0)

# 2) Lookup username
db_path = os.path.join(os.path.dirname(__file__), 'data', 'servers.db')
conn = sqlite3.connect(db_path); cur = conn.cursor()
cur.execute("SELECT username FROM sessions WHERE session_id = ?", (session_id,))
row = cur.fetchone()
if not row:
    print("Status: 400 Bad Request\nContent-Type: text/plain\n\nInvalid session")
    sys.exit(0)
owner = row[0]

# 3) Parse description
form = cgi.FieldStorage()
desc = form.getfirst('desc','').strip()
if not desc:
    print("Status: 400 Bad Request\nContent-Type: text/plain\n\nMissing desc")
    sys.exit(0)

# 4) Insert new server with ready=0 (for true background, but here we’ll mark ready=1)
inst_id = f"{owner}-{int(time.time())}"
cur.execute(
    "INSERT INTO servers (owner, description, instance_id, ready) VALUES (?, ?, ?, 1)",
    (owner, desc, inst_id)
)
new_id = cur.lastrowid
conn.commit()
conn.close()

# 5) Redirect to status JSON
print("Status: 303 See Other")
print(f"Location: /api/servers.py/{new_id}\n")
