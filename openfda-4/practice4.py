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
        if self.path == "/" :
            print("Searching...")
            with open("search.html", 'r') as f:
                message = f.read()
                # Write content as utf-8 data
                self.wfile.write(bytes(message, "utf8"))
        #When the client introduces a drug and a limit in the html, a new search is taking place that includes the word search in the path
        elif 'search' in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            #From the search path we remove "/search" and the "?", then we separate each word by ""
            search = self.path.strip('/search?').split('""')
            #Now we assign each variable its correspondent information
            drug_label = search[0].split('=')[1]
            limit_drug = search[1].split('=')[1]

            url = "/drug/label.json?search=active_ingredient:"+ drug_label + '&' + 'limit=' + limit_drug

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")

            conn.close()
            repos = json.loads(repos_raw)
            self.wfile.write(bytes(json.dumps(repos), "utf8"))
        return

#Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("Server stopped!")