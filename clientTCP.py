from socket import *
import math

BUFFERSIZE = 10	

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
	
################################# Start of main Program #################################

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

print 'Connected to server on port : ', serverPort
#input User Query
fileName = raw_input('Input File Name to query : ')

#format the Query
httpQuery = getHttpRequest(fileName)

#send query via the Socket
sendData(httpQuery,clientSocket)

#get Response
data = receiveData(clientSocket)

#decode Response
data = data.split('\n')
state = int(data[0].split(' ')[1])

if state == 400:
	print 'Bad request.'
if state == 404:
	print 'File Not Found!'
if state == 200:
	fileData = ''
	for i in data[4:]:
		fileData = fileData + i + '\n'

	f = open(fileName,'w')
	f.write(fileData)
	f.close()
	print 'File ',fileName,' created'
#close the Socket
clientSocket.close()
'Socket Closed.\nConnection Terminated!'
