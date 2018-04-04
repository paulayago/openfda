# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8020
import http.server
import socketserver
import http.client
import json

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


header = "<ol>"+"\n"
finish = "</ol>"+"\n"

with open("htmlpractice3.html", "w") as f:
    f.write(header)
    for i in drugs:
        elemlist = "<li>" + i + "</li>" + "\n"
        f.write(elemlist)
    f.write(finish)

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        with open("htmlpractice3.html", "r") as f:
            message=f.read()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

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
