from socket import *
import math

BUFFERSIZE = 1024

def decodeHttpRequest(query):
	state = 200
	fileNameList = query.strip().split(' ')
	
	fileName = ''
	print len(fileNameList)-2
	for i in fileNameList[1:len(fileNameList)-1]:
		fileName = fileName + i

	if fileNameList[0] != 'GET':
		state = 400
	if fileNameList[len(fileNameList)-1] == 'HTTP/1.0':
		state = 400
	
	return state,fileName
	
def fileRead(file):
	return file.read()

def sendData(data, sendSocket):
	size = len(data)
	numberOfPackets = int(math.ceil((size*1.0/BUFFERSIZE)))
	sendSocket.send(str(numberOfPackets))
	packetNumber = 0
	while packetNumber < numberOfPackets:
		sendSocket.send(data[BUFFERSIZE*packetNumber:BUFFERSIZE*(packetNumber+1)])
		packetNumber = packetNumber + 1
	
	
def receiveData(receiveSocket):
	n = int(receiveSocket.recv(BUFFERSIZE))
	data = ''
	while n > 0:
		data = data + receiveSocket.recv(BUFFERSIZE)
		n = n - 1
	return data


#define Server port as 8794
serverPort = 8794

# create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# bind the socket
serverSocket.bind(('',serverPort))

# Wait for incoming sockets/requests
serverSocket.listen(1)

# Check if the server is working
print 'Server Started on Port ',serverPort
while 1:
	# Accept the incoming socket and create a connection socket
	connectionSocket, addr = serverSocket.accept()
	
	# Recieve data from the incoming socket
	query = receiveData(connectionSocket)
	
	# get file Name from the Http Query request
	state,fileName = decodeHttpRequest(query)

	# Tester Code
	f = open(fileName)
	data = f.read()
	# Send processed data to the client
	sendData(data,connectionSocket)
	# Close the connection socket
	connectionSocket.close()
