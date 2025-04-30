#!/usr/bin/env python3
import cgi, os, sqlite3, sys, time, json

# 1) Parse form data
form  = cgi.FieldStorage()
owner = form.getfirst('user','').strip()
desc  = form.getfirst('desc','').strip()
if not owner or not desc:
    print("Status: 400 Bad Request")
    print("Content-Type: application/json\n")
    print(json.dumps({"error":"Missing user or desc"}))
    sys.exit(0)

# 2) Fake instance_id and mark ready immediately
inst_id = f"{owner}-{int(time.time())}"
ready   = 1

# 3) Insert into SQLite
script_dir = os.path.dirname(os.path.realpath(__file__))
db_path    = os.path.join(script_dir, 'data', 'servers.db')
conn = sqlite3.connect(db_path)
cur  = conn.cursor()
cur.execute(
  "INSERT INTO servers (owner,description,instance_id,ready) VALUES (?,?,?,?)",
  (owner, desc, inst_id, ready)
)
new_id = cur.lastrowid
conn.commit()
conn.close()

# 4) Redirect to JSON endpoint
print("Status: 303 See Other")
print(f"Location: /api/servers.py/{new_id}\n")
