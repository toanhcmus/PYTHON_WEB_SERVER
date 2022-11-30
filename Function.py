import socket

CHUNK_SIZE = 65654

def ReadRequest(client):
	request = ""
	client.settimeout(1)
	try:
		request = client.recv(1024).decode()
		while (request):
			request = request + client.recv(1024).decode()
	except socket.timeout():
		if not request:
			print("No request!")
			print("===================================")
	finally:
		return request

def Homepage(client):
	f = open("index.html", "rb")
	L = f.read()
	header ="HTTP/1.1 200 OK\r\nContent-Length: {0:d}\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n".format(len(L))
	header += L.decode()
	client.send(bytes(header, 'utf-8'))
	print("Done!")

def Images(client):
	f = open ("images.html", "rb")
	L = f.read()
	header ="HTTP/1.1 200 OK\r\nContent-Length: {0:d}\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n".format(len(L))
	header += L.decode()
	client.send(bytes(header, 'utf-8'))
	print("Done!")

def error404(client):
	f = open ("404.html", "rb")
	L = f.read()
	header ="HTTP/1.1 404 Not Found\r\nContent-Length: %d\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"%len(L) 
	header += L.decode()
	client.send(bytes(header, 'utf-8'))
	print("Done!")

def error401(client):
	f = open ("401.html", "rb")
	L = f.read()
	header ="HTTP/1.1 401 Unauthorized\r\nContent-Length: %d\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"%len(L) 
	header += L.decode()
	client.send(bytes(header, 'utf-8'))
	print("Done!")

def CSS(client, filename):
	f = open (filename, "rb")
	L = f.read()
	header ="HTTP/1.1 200 OK\r\nContent-Length: %d\r\nContent-Type: text/css\r\nConnection: close\r\n\r\n"%len(L) 
	header += L.decode()
	client.send(bytes(header, 'utf-8'))
	print("Done!")

def PostRequest(client, requestcontent):
	if "uname=admin&psw=123456" in requestcontent:
		Images(client)
	else:
		error401(client)

def ImagesFile(client, filename):
	print("File to open:" + filename)
	f=open(filename,"rb")
	if (".png" in filename):
		header="HTTP/1.1 200 OK\r\nContent-Type: image/png\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n\r\n"
	if (".jpg" in filename or ".jepg" in filename):
		header="HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n\r\n"
	
	body = "".encode()
	data = f.read(CHUNK_SIZE)
	while (data):
		body += ("{:x}\r\n".format(len(data))).encode('utf-8')
		body += data
		body += "\r\n".encode()
		data = f.read(CHUNK_SIZE)
	body += "0\r\n\r\n".encode('utf-8')
	header = header.encode('utf-8') + body
	client.send(header)
	print("Done!")
	f.close()
	

def FileType(client, requestpath):
	files = ["404.png","1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","pexels-quang-nguyen-vinh-4544171.jpg","pexels-quang-nguyen-vinh-5118664.jpg","pexels-quang-nguyen-vinh-6136262.jpg","pexels-quang-nguyen-vinh-6877795.jpg"]
	for x in files:
		if x in requestpath:
			if "404.png" in x:
				x = "404img/"+x
			elif ".png" in x:
				x = "avatars/"+x
			elif ".jpg" in x:
				x = "images/" + x
			ImagesFile(client,x)
			return

def handleRequest(client, requestmethod, requestpath, requestcontent):
		if requestmethod == "GET" and requestpath in ["/", "/index.html"]:
			Homepage(client)
			print("===================================")
		elif requestmethod == "POST":						
			PostRequest(client, requestcontent)
			print("===================================")
		elif requestmethod == "GET" and "/css" in requestpath:
			file = requestpath[1:]
			CSS(client, file)
			print("===================================")
		elif requestmethod == "GET" and "/images" in requestpath  and ".jpg" in requestpath:
			FileType(client, requestpath)
			print("===================================")
		elif requestmethod == "GET" and ("/avatars" in requestpath or "/404img" in requestpath) and ".png" in requestpath:
			FileType(client, requestpath)
			print("===================================")
		elif requestmethod == "GET" and "/favicon.ico" in requestpath:
			print("Not found favicon.ico!")
			print("===================================")
		else:
			error404(client)
			print("===================================")