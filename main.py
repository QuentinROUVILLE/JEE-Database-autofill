# Script args need to be in the following order:
# 1. Database name
# 2. Database username
# 3. Database password
# 4. Database host
# 5. Database port
# 6. GoogleMaps API key
import random

import psycopg2
import sys
import json
import time
from urllib.request import urlopen
from meals import meals

db_name = sys.argv[1]
db_user = sys.argv[2]
db_password = sys.argv[3]
db_host = sys.argv[4]
db_port = sys.argv[5]
gmap_api_key = sys.argv[6]
max_pages = 3

postgres = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

cursor = postgres.cursor()
next_page_token = ""

for page in range(0, max_pages):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=48.858705,2.342865&radius=3000&type=restaurant&key=' + gmap_api_key + '&pagetoken=' + next_page_token
    response = urlopen(url)

    string = response.read().decode('utf-8')
    json_obj = json.loads(string)

    try:
        next_page_token = json_obj['next_page_token']
    except KeyError:
        next_page_token = ""

    for place in json_obj['results']:
        cursor.execute("INSERT INTO location (latitude, longitude) VALUES (%s, %s)",
                       (place['geometry']['location']['lat'], place['geometry']['location']['lng']))

        cursor.execute("SELECT id FROM location WHERE latitude = %s AND longitude = %s",
                       (place['geometry']['location']['lat'], place['geometry']['location']['lng']))
        cursor.execute("INSERT INTO restaurant (name, location_id) VALUES (%s, %s)",
                       (place['name'], cursor.fetchone()[0]))

        cursor.execute("SELECT id FROM restaurant WHERE name = %s", (place['name'],))
        restaurant_id = cursor.fetchone()[0]
        for meal in range(0, 3):
            random_meal = meals[int(random.uniform(0, len(meals) - 1))]
            print(random_meal)
            cursor.execute("INSERT INTO meal (name, price, restaurant_id) VALUES (%s, %s, %s)", (random_meal['name'], random.uniform(random_meal['minprice'], random_meal['maxprice']), restaurant_id))

        postgres.commit()

        print("Inserted location: " + str(place['geometry']['location']['lat']) + "," + str(place['geometry']['location']['lng']))

    if next_page_token == "" or page == max_pages - 1:
        break
    time.sleep(3)

print("Tout s'est tr??s bien pass?? !")