from socket import *

serverName = 'localhost'
serverPort = 8794

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Enter your message -> ')
clientSocket.sendto(message,(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print modifiedMessage
clientSocket.close()