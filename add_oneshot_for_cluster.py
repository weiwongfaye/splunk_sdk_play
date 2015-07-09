import splunklib.client as client
import splunklib.results as results
import time
import sys
import random
HOST = ["10.66.129.93","10.66.129.174","10.66.129.42","10.66.129.75","10.66.129.78"]
PORT = 8089
USERNAME = "admin"
PASSWORD = "password"

for i in range(500):
    indexstr = 'jack_test_%s' % str(i)
    host_index = random.randint(0,4)
    # Create a Service instance and log in
    service = client.connect(
        host=HOST[host_index],
        port=PORT,
        username=USERNAME,
        password=PASSWORD)

    # Print installed apps to the console to verify login
    #for app in service.apps:
    #    print app.name

    # list of indexes
    indexes = service.indexes

    for index in indexes:
        count = index["totalEventCount"]
        print "%s (events: %s)" % (index.name, count)
    myindexes =  service.indexes[indexstr]
    #uploadme = '\\\\10.66.129.90\\testshare\\xaa'
    uploadme = 'C:\\xaa'
    myindexes.upload(uploadme)

    # List the indexes and their event counts
    for index in indexes:
        count = index["totalEventCount"]
        print "%s (events: %s)" % (index.name, count)
