from socket import *
import math

BUFFERSIZE = 1024	

def getHttpRequest(query):
	query = 'GET '+ query + ' HTTP/1.0'
	return query

def sendData(data, sendSocket):
	size = len(data)
	numberOfPackets = int(math.ceil((size*1.0/BUFFERSIZE)))
	sendSocket.send(str(numberOfPackets))
	packetNumber = 0
	while packetNumber < numberOfPackets:
		sendSocket.send(data[BUFFERSIZE*packetNumber:BUFFERSIZE*(packetNumber+1)])
		packetNumber = packetNumber + 1

def receiveData(clientSocket):
	n = int(clientSocket.recv(BUFFERSIZE))
	data = ''
	while n > 0:
		data = data + clientSocket.recv(BUFFERSIZE)
		n = n - 1
	return data
	
#User Input for 
serverName = raw_input('Enter Server Host Name : ')
if (serverName == ''):
	serverName = 'localhost'
serverPort = raw_input('Enter Server Port Number : ') 
if (serverPort == ''):
	serverPort = 8794
else:
	serverPort = int(serverPort)
	
#Create a TCP socket. 
clientSocket = socket(AF_INET, SOCK_STREAM)

#connect to the server
clientSocket.connect((serverName,serverPort))

#input User Query
query = raw_input('Input User Query :')

#format the Query
httpQuery = getHttpRequest(query)

#send query via the Socket
sendData(httpQuery,clientSocket)

#get Response
data = receiveData(clientSocket)
#print Response
print '\n'
print data
#close the Socket
clientSocket.close()
