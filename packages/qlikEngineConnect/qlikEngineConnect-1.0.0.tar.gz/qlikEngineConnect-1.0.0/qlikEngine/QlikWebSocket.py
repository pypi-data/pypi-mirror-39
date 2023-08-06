from websocket import create_connection
import ssl
import json
import requests
import urllib.request

class QlikWebSocket():
	def __init__(self, senseHost, #qlikapp.companyname.companyname.domain
	privateKeyPath , # Path to certificates on the local machine. If on windows, then use '\\'
	userDirectory, #Found from the QMC, contact your administrator
	UserId #User id
	):
		self.version = "1.0.0"
		self.senseHost = senseHost
		self.privateKeyPath = privateKeyPath
		## userDirectory and userId can be found at QMC -> Users  
		self.userDirectory, self.userId = userDirectory, UserId
		
		url = "wss://" + self.senseHost + ":4747/app"  # valid
		certs = ({"ca_certs": self.privateKeyPath + "root.pem",
					"certfile": self.privateKeyPath + "client.pem",
					"keyfile": self.privateKeyPath + "client_key.pem",
					"cert_reqs" : ssl.CERT_NONE,
					"server_side": False
					})
		ssl.match_hostname = lambda cert, hostname: True
		self.ws = create_connection(url, sslopt=certs,
							header={'X-Qlik-User: UserDirectory=%s; UserId=%s'% (self.userDirectory, self.userId)})
		self.ws.recv()
		print("Connection successful")


	def send_json(self, json, # the json that you want to send to Qlik engine. Can be found from the Engine API explorer in dev hub.
		print_console=False # Pass True if you want to print thte response to the console
		):
		self.ws.send(json)
		self.response = self.ws.recv()
		if print_console == True: 
			print(self.response)
		return self.response