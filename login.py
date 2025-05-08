#!/usr/bin/env python3
import cgi, os, sqlite3, sys, uuid

# 1) Read the username from the form
form = cgi.FieldStorage()
user = form.getfirst('user','').strip()
if not user:
    print("Status: 400 Bad Request\nContent-Type: text/plain\n\nMissing user")
    sys.exit(0)

# 2) Generate a session token
session_id = str(uuid.uuid4())

# 3) Store it in the sessions table
db_path = os.path.join(os.path.dirname(__file__), 'data', 'servers.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute(
    "INSERT INTO sessions (session_id, username) VALUES (?, ?)",
    (session_id, user)
)
conn.commit()
conn.close()

# 4) Set a cookie and redirect to the main page (/index.py)
print("Status: 303 See Other")
print(f"Set-Cookie: session={session_id}; Path=/")
print("Location: /index.py\n")
