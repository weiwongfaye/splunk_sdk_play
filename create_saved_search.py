import splunklib.client as client
import splunklib.results as results
import time
import sys
HOST = "10.66.4.66"
PORT = 8089
USERNAME = "admin"
PASSWORD = "test1234"

# Create a Service instance and log in
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

# Print installed apps to the console to verify login
#for app in service.apps:
#    print app.name

jobs = service.jobs
kwargs_blockingsearch = {"exec_mode": "blocking"}
job = jobs.create("|rest splunk_server=local /services/search/distributed/peers|search cluster_label=jacktest|search host=systest-1-idx3 OR host=systest-1-idx2|fields bundle_versions",**kwargs_blockingsearch)
#time.sleep(10)
print job.results()

print "parsing results"
for result in results.ResultsReader(job.results()):
    print result
    print "results"
    print result["bundle_versions"][1]
#time.sleep(10)
#print job.results()

saved_searches = service.saved_searches
#for i in range(10):
    #saved_searches.create("jacktest%s_saved_search" % str(i),'search _internal | head 1')

#assert 'jacktest1_saved_search' in saved_searches
#saved_searches.delete('jacktest1_saved_search')
#assert 'my_saved_search' not in saved_searches

#for item in saved_searches:
#    print item['_state']["title"]

#saved_searches.delete('jack_saved_search')
for item in saved_searches:
    print item.name
    print item['_state']['title']
#saved_searches.create("jacktestnew_saved_search",'search index=_internal | head 1')

# Retrieve the new search
mysavedsearch = service.saved_searches["jacktestnew_saved_search"]

# Print the properties of the saved search
print "Description:         ", mysavedsearch["description"]
print "Is scheduled:        ", mysavedsearch["is_scheduled"]
print "Cron schedule:       ", mysavedsearch["cron_schedule"]
print "Next scheduled time: ", mysavedsearch["next_scheduled_time"]

# Specify a description for the search
# Enable the saved search to run on schedule
# Run the search on Saturdays at 4:15am
# Search everything in a 24-hour time range starting June 19, 12:00pm
kwargs = {"description": "This is a test search",
        "is_scheduled": True,
        "cron_schedule": "15 4 * * 6"}
        #"earliest_time": "2014-07-07T12:00:00.000-07:00",
        #"latest_time": "2014-07-08T12:00:00.000-07:00"}

# Update the server and refresh the local copy of the object
mysavedsearch.update(**kwargs).refresh()

# Print the properties of the saved search
print "Description:         ", mysavedsearch["description"]
print "Is scheduled:        ", mysavedsearch["is_scheduled"]
print "Cron schedule:       ", mysavedsearch["cron_schedule"]
print "Next scheduled time: ", mysavedsearch["next_scheduled_time"]


job = mysavedsearch.dispatch()


# Create a small delay to allow time for the update between server and client
time.sleep(2)

# Wait for the job to finish--poll for completion and display stats
while True:
    job.refresh()
    stats = {"isDone": job["isDone"],
             "doneProgress": float(job["doneProgress"])*100,
              "scanCount": int(job["scanCount"]),
              "eventCount": int(job["eventCount"]),
              "resultCount": int(job["resultCount"])}
    status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
              "%(eventCount)d matched   %(resultCount)d results") % stats

    sys.stdout.write(status)
    sys.stdout.flush()
    if stats["isDone"] == "1":
        break
    sleep(2)

# Display the search results now that the job is done
jobresults = job.results()
for result in results.ResultsReader(job.results()):
    print result
