from socket import *
import math

BUFFERSIZE = 1024

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
	data = receiveData(connectionSocket)
	
	# Send processed data to the client
	sendData(data,connectionSocket)
	# Close the connection socket
	connectionSocket.close()
