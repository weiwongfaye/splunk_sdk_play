import splunklib.client as client
import splunklib.results as results
import time
import sys
HOST = "10.66.129.79"
PORT = 8089
USERNAME = "admin"
PASSWORD = "notchangeme"

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

# Print installed apps to the console to verify login

saved_searches = service.saved_searches

#saved_searches.delete('jack_saved_search')
for item in saved_searches:
    print item.name
    if item.name[0:3] == "sys":
        saved_searches.delete(item.name)





