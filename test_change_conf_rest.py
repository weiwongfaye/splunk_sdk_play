import requests
from requests.auth import HTTPBasicAuth
import json
import paramiko
import time


Hosts = ['localhost',]
PLATFORM = "WINDOWS"

if PLATFORM == "WINDOWS":
	SPLUNK_HOME = "/cygdrive/c/splunk"
	SPLUNK_EXEUTABLE = os.path.join(SPLUNK_HOME,'bin','splunk')
else:
	SPLUNK_HOME = '/export/usr/eserv/splunk'
	SPLUNK_EXEUTABLE = os.path.join(SPLUNK_HOME,'bin','splunk')


for host in Hosts:

	print '#'*100
	print host
	# https://localhost:8089/servicesNS/nobody/system/configs/conf-server/genera
	config_server_uri = 'https://{0}:8089/servicesNS/nobody/system/configs/conf-server/general'.format(host)
	config_web_uri = 'https://{0}:8089/servicesNS/nobody/system/configs/conf-web/settings'.format(host)

	payload_server ={"listenOnIPv6":"only"}
	payload_web ={"listenOnIPv6":"yes","mgmtHostPort":"[::1]:8089"}

	# Use verify=False if your root CA can't be verified.
	# Or you can specify verify = '../mycert.pem'
	r = requests.post(config_server_uri,auth=('admin','notchangeme'),data=payload_server,verify =False)
	print r.text
	r = requests.post(config_web_uri,auth=('admin','notchangeme'),data=payload_web,verify =False)    
	print r.text


	# restart machine
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username='xxx', password='xxx')
	stdin, stdout, stderr = ssh.exec_command("{0} restart -f".format(SPLUNK_EXEUTABLE))

	print stdout.readlines()[0]
