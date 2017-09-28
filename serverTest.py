from socket import *

serverPort = 8794
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print "Server Started and Ready!"

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	print message
	serverSocket.sendto('You Got it Correct!',clientAddress)

