from socket import *
import math

BUFFERSIZE = 1024	

def getHttpRequest(query):
	query = 'SET /'+ query + ' HTTP/1.0\n'
	return query

def sendData(data, sendSocket):	
	sendSocket.send(data)
		

def receiveData(clientSocket):
	#n = int(clientSocket.recv(BUFFERSIZE))
	temp = clientSocket.recv(BUFFERSIZE)
	data = temp
	while temp:
		temp = clientSocket.recv(BUFFERSIZE)
		data = data + temp
		
	return data
	
################################# Start of main Program #################################
try:
	#User Input for 
	serverName = raw_input('Enter Server Host Name : ')
	if (serverName == ''):
		serverName = 'localhost'
	serverPort = raw_input('Enter Server Port Number : ') 
	if (serverPort == ''):
		serverPort = 8794
	else:
		serverPort = int(serverPort)
except Exception as e:
	print 'Exit Gracefully!'

try:		
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
		for i in data[3:]:
			fileData = fileData + i + '\n'

		f = open(fileName,'w')
		f.write(fileData)
		f.close()
		print 'File ',fileName,' created'
	#close the Socket
	clientSocket.close()
	'Socket Closed.\nConnection Terminated!'
except Exception as e:
	print 'Exit Gracefully!'
	connectionSocket.close()
