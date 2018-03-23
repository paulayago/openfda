# A basic web server using sockets

#donde pone local host poner el ip luego lo abres con el terminal y te sale un ip y 
#un puerto eso se copia y pega en google y entre el ip y el puerto sale un espacio y lo 
#cambias por dos puntos y ya esta 
import socket

PORT = 8096
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):
	print(clientsocket)
	bytes = clientsocket.recv(1024)
	print(bytes)
	string = bytes.decode()
	print(string)
	lines = string.split("\n")
	if lines[0]=='GET / HTTP/1.1\r':
		with open("new 1.html", 'r') as f:
			paula = f.read()
		web_contents = paula
		web_headers = "HTTP/1.1 200"
		web_headers += "\n" + "Content-Type: text/html"
		web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
		clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
		clientsocket.close()
	elif lines[0]== 'GET /new HTTP/1.1\r':
		with open("new 2.html", 'r') as f:
			paula = f.read()
		web_contents = paula
		web_headers = "HTTP/1.1 200"
		web_headers += "\n" + "Content-Type: text/html"
		web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
		clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
		clientsocket.close()
	

	


# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
# Let's use better the local interface name
hostname = "10.10.104.173"
try:
    serversocket.bind((hostname, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print ("Waiting for connections at %s %i" % (hostname, PORT))
        (clientsocket, address) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a non threaded server
        process_client(clientsocket)

except socket.error:
    print("Problemas using port %i. Do you have permission?" % PORT)
