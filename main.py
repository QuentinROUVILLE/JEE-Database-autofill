# Script args need to be in the following order:
# 1. Database name
# 2. Database username
# 3. Database password
# 4. Database host
# 5. Database port
# 6. GoogleMaps API key

import psycopg2
import sys
import json
from urllib.request import urlopen

db_name = sys.argv[1]
db_user = sys.argv[2]
db_password = sys.argv[3]
db_host = sys.argv[4]
db_port = sys.argv[5]
gmap_api_key = sys.argv[6]

postgres = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

cursor = postgres.cursor()
cursor.execute("INSERT INTO location VALUES (4, 4.0, 2.0);")
postgres.commit()