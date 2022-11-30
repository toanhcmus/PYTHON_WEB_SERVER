import socket
from Function import *
		
IP = ''
PORT = 8080

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((IP, PORT))
SERVER.listen(5)
print("Waiting for client...")

def __main():
	while True:
		client, addr = SERVER.accept()
		print("Client ", addr,"connected!")
		request = ReadRequest(client)
		if request != "":
			print("--> Got a request")
			requestArray = request.split("\n")
			#print request
			print(requestArray[0])
			requestmethod = requestArray[0].split(" ")[0]
			requestpath = requestArray[0].split(" ")[1]
			requestcontent = requestArray[-1]
			if (requestcontent != ""):
				print(requestcontent)
			handleRequest(client, requestmethod, requestpath, requestcontent)
		client.shutdown(socket.SHUT_RD)
	client.close()
	
if __name__ == "__main__":
	__main()

