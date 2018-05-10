# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            print ("Searching...")
            # Send message back to client
            with open("search.html", "r") as f:
                message = f.read()
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            print("File served!")

        #If the word search is in the search path, then we need to separate the information regarding the drug label and
        #the drug limit
        elif "search" in self.path:
            headers = {'User-Agent': 'http-client'}
            #Expecifying the web page where we need to obtain the information from
            conn = http.client.HTTPSConnection("api.fda.gov")
            #We delete the word search and the ? form the search path and separate the other words by ""
            search = self.path.strip('/search?').split('""')
            #Now we assign each varibale the correspondant information
            drug_label = search[0].split('=')[1]
            drug_limit = search[1].split('=')[1]
            print("The client has succesfully made a request!")

            url = "/drug/label.json?search=active_ingredient:" + drug_label + '&' + 'limit=' + drug_limit
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)
            self.wfile.write(bytes(json.dumps(repos), "utf8"))
        return
# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")