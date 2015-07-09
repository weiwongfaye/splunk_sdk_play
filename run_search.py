import splunklib.client as client
import splunklib.results as results
import time
HOST = "10.66.129.90"
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
