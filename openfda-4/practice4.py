import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
drugs = []

for i in range (len (repos['results'])):
    aspirin = repos['results'][i]
    if (aspirin['openfda']) == {}:
        drugs.append("")
    else:
        drugs.append(aspirin["openfda"]["generic_name"][0])

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


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
            # Send message back to client
            with open("search.html") as f:
                message = f.read()
        # Write content as utf-8 data
        elif self.path == "/new":
            with open("new.html", "r") as f:
                new = f.read()
                message = new
        else:
            with open("error.html", "r") as f:
                error = f.read()
                message = error

        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
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