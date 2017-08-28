import sys
import socket
import os
import pprint

rHost = "54.227.162.31"
rPort = 6675
myPort = 6703

#Function to setup TCP Proxy
def startProxy():
	proxy = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		proxy.bind(('',myPort))
	except:
		pprint.pprint("Proxy not activated")
		sys.exit()

	pprint.pprint("Proxy successfully activated")
	proxy.listen(5)

	cSocket,addr = proxy.accept()
	pprint.pprint("Connection requested from: ")
	pprint.pprint("Address - " + str(addr))
	pprint.pprint("-------------------------------------------------------")
	proxyFunctions(cSocket,addr)
	return

#Function to receive and forward packets between Client and RHost
def proxyFunctions(cSocket, addr):
	pprint.pprint("Connection Accepted from: " + str(addr))

	#Prepare socket to rHost, rPort
	rSocket = prepRemoteSock(rHost,rPort)

	count = 0
	
	try:
		while 1:
			#Get Request Packet from Client in Custom Protocol Format
			cbuffer = getFromClient(cSocket)
			count += 1

			if (len(cbuffer) > 0):

				#Print Data Received
				pprint.pprint("Received " + str(len(cbuffer)) + " bytes of data")
				pprint.pprint("Packet No. - " + str(count))
				pprint.pprint(cbuffer)
				
				#Log the Packet Data Received
				cRequestLog(cbuffer,count)

				# Make Changes to Request Packet
				#if (count == 1):
					#temp = makeChange(cbuffer)
					#cbuffer = temp
					#pprint.pprint("Modified Packet -")
					#pprint.pprint(cbuffer)	
				
				# Forward Request Packet to rHost, rPort
				rSocket.send(cbuffer)
				pprint.pprint("Packet forwarded to Remote Host")
				pprint.pprint("|||||||||||||||||||||||||||||||||||||||||||||||||||||||")
			
			#Get Response Packet from Remote Host in Custom Protocl Format
			rbuffer = getFromRemote(rSocket)
			count += 1 

			if (len(rbuffer) > 0):

				#Print Response Data Received
				pprint.pprint("Received " + str(len(rbuffer)) + " bytes of data")
				pprint.pprint("Packet No. - " + str(count))
				pprint.pprint(rbuffer)

				#Log the Response Packet Data Received
				rResponseLog(rbuffer,count)

				#Make Changes to Response Packet
				#if (count == 10):
					#temp = makeChange(rbuffer)
					#rbuffer = temp
					#pprint.pprint("Modified Packet -")
					#pprint.pprint(rbuffer)

				#Forward Response Packet back to Client
				cSocket.send(rbuffer)
				pprint.pprint("Packet forwarded back to Client")
				pprint.pprint("|||||||||||||||||||||||||||||||||||||||||||||||||||||||")

	except KeyboardInterrupt:
		rSocket.close()
		cSocket.close()
		sys.exit()

	except Exception as e:
		pprint.pprint("Error Message - " + str(e))


	rSocket.close()
	cSocket.close()
	pprint.pprint("Exiting from Current Socket Connections")
	return

#Get Packet Data from Client - Request Packet
def getFromClient(cSocket):
	pprint.pprint("Currently receiving data from client")
	buffer = ''

	data = cSocket.recv(4096)
	if (len(data) > 0):
		buffer += data
	else:
		pprint.pprint("No Data Received")

	return buffer

#Get Packet Data from Remote Host - Response Packet
def getFromRemote(rSocket):
	pprint.pprint("Currently receiving data from Remote Host")
	buffer = ''
	data = rSocket.recv(4096)
	if (len(data) > 0):
		buffer += data
	else:
		pprint.pprint("No Data Received")
	return buffer

#Make Changes to Packet Data
def makeChange(buffer):
	temp = "\x00\x04\x00" + buffer[4:]
	return temp

#Log Request Packets Received from Client
def cRequestLog(buf,count):
	f = open("Request_Log.txt","a")
	f.write("Request Packet")
	f.write("\n")
	f.write("Packet No. -" + str(count))
	f.write("\n")
	f.write(buf)
	f.write("\n")
	f.write("------------------------------------------------------")
	f.write("\n")
	f.close()
	return

#Log Response Packets Received from Remote Host
def rResponseLog(buf,count):
	f = open("Response_Log.txt","a")
	f.write("Response Packet")
	f.write("\n")
	f.write("Packet No. -" + str(count))
	f.write("\n")
	f.write(buf)
	f.write("\n")
	f.write("------------------------------------------------------")
	f.write("\n")
	f.close()
	return

#Create Socket to communicated with rHost,rPort
def prepRemoteSock(rHost,rPort):
	rSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	rSocket.connect((rHost,rPort))
	return rSocket

if __name__ == '__main__':
	startProxy()
