from socket import *
import math
import os

BUFFERSIZE = 1024

def getHttpResponse(state,fileName):
	if state == 400:
		return 'HTTP/1.0 400 Bad Request'
	else:
		if state == 404:
			return 'HTTP/1.0 404 Not Found'
		else:
			f = open(fileName,'rb')
			data = f.read()
			size = len(data)
			return 'HTTP/1.0 200 OK\nContent-Length: '+str(size)+'\n\n'+data


def decodeHttpRequest(query):
	state = 200
	queryList = query.strip().split('\n')[0]
	fileNameList = queryList.strip().split(' ')	
	fileName = ''
	for i in fileNameList[1:len(fileNameList)-1]:
		fileName = fileName + i
	fileName = fileName[1:]
	
	if ((fileNameList[0] != 'GET') or (fileNameList[len(fileNameList)-1] != 'HTTP/1.0')):
		state = 400	
	else:
		if (os.path.isfile(fileName) == False):
			state = 404
	return state,fileName
	
def fileRead(file):
	return file.read()

def sendData(data, sendSocket):
	size = len(data)
	
	numberOfPackets = int(math.ceil((size*1.0/BUFFERSIZE)))	
	packetNumber = 0
	while packetNumber < numberOfPackets:
		sendSocket.send(data[BUFFERSIZE*packetNumber:BUFFERSIZE*(packetNumber+1)])
		packetNumber = packetNumber + 1
		
	
	
def receiveData(receiveSocket):
	#n = int(receiveSocket.recv(BUFFERSIZE))
	data = receiveSocket.recv(BUFFERSIZE)	
	return data

################################# Start of main Program #################################


serverPort = int(raw_input('Enter Port Number to setup the server : '))
# create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# bind the socket
serverSocket.bind(('',serverPort))

print 'Server started on port : ', serverPort

# Wait for incoming sockets/requests
serverSocket.listen(1)


while 1:
	try :
		# Accept the incoming socket and create a connection socket
		connectionSocket, addr = serverSocket.accept()
		
		# Recieve data from the incoming socket
		query = receiveData(connectionSocket)
		print query
		
		# get file Name from the Http Query request
		state,fileName = decodeHttpRequest(query)
		
		#generate response
		data = getHttpResponse(state,fileName)
		
		# Send processed data to the client
		sendData(data,connectionSocket)
		# Close the connection socket
		connectionSocket.close()
	except:
		print 'Exit Gracefully!'
		connectionSocket.close()
