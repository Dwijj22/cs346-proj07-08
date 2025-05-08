#!/usr/bin/env python3
import cgi, os, sqlite3, sys

# 1) Read the “id” parameter from the query string
form = cgi.FieldStorage()
sid = form.getfirst('id','').strip()
if not sid.isdigit():
    print("Status: 400 Bad Request")
    print("Content-Type: text/plain\n")
    print("Invalid server ID")
    sys.exit(0)

# 2) Delete that server row from the database
db_path = os.path.join(os.path.dirname(__file__), 'data', 'servers.db')
conn = sqlite3.connect(db_path)
cur  = conn.cursor()
cur.execute("DELETE FROM servers WHERE id = ?", (sid,))
conn.commit()
conn.close()

# 3) Redirect back to the HTML list
print("Status: 303 See Other")
print("Location: /list_servers.py\n")
