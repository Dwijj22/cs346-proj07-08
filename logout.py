#!/usr/bin/env python3
import os, sqlite3, sys

# 1) Extract the “session” cookie
cookie = os.environ.get('HTTP_COOKIE','')
session_id = None
for part in cookie.split(';'):
    if part.strip().startswith('session='):
        session_id = part.split('=',1)[1]
        break

# 2) Delete it from the sessions table (if present)
if session_id:
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'servers.db')
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

# 3) Expire the cookie and redirect to login.html
print("Status: 303 See Other")
print("Set-Cookie: session=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
print("Location: /login.html\n")
