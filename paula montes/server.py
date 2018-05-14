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

        #We use this step in order to change all the different status codes for all the options that exist

        if self.path == "/" or 'searchDrug' in self.path or 'searchCompany' in self.path or 'listDrugs' in self.path or 'listCompanies' in self.path or 'listWarnings' in self.path:
            status_code = 200
        elif 'redirect' in self.path:
            status_code = 302
        elif 'secret' in self.path:
            status_code = 401
        else:
            status_code = 404

        self.send_response(status_code)

        if self.path == "/" or 'searchDrug' in self.path or 'searchCompany' in self.path or 'listDrugs' in self.path or 'listCompanies' in self.path or 'listWarnings' in self.path:
            self.send_header('Content-type', 'text/html')
        elif 'redirect' in self.path:
            self.send_header('Location', 'http://localhost:8000/')
        elif 'secret' in self.path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')


        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        def active_ingredient():  # We use this definition to search for a drug and a limit

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            info = self.path.strip('/search?').split('&')  # We remove '/search?' and separate the rest at '&'
            drug = info[0].split('=')[1]
            if "limit" in self.path:
                limit = info[1].split('=')[1]
                if limit == "":
                    limit = "10"
            else:
                limit = "10"
            print("The client has successfully made a request!")

            url = "/drug/label.json?search=active_ingredient:" + drug + '&' + 'limit=' + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            my_list = []
            a = 0
            start_list = "<head>" + "<h2>" + "These are the brand names of the drugs that you are looking for:" + '<body style="background-color: #ff99bb">' + "</h2>" + "</head>" "<ol>" + "\n"
            nlimit = int(limit)

            while a < nlimit:
                try:
                    my_list.append(repos['results'][a]["openfda"]['brand_name'][0])
                    a += 1
                except:
                    my_list.append("Not known")
                    print("Drugs with this active ingredient are not found")
                    a += 1

            with open ("data_drugs.html", "w") as f:
                f.write(start_list)
                for element in my_list:
                    list_elements = "<t>" + "<li>" + element
                    f.write(list_elements)


        def manufacturer_name():   # We use this definition to search for a manufacturer and a limit

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            info = self.path.strip('/search?').split('&')  # We remove '/search?' and separate the rest at '&'
            manufacturer_name = info[0].split('=')[1]
            if "limit" in self.path:
                limit = info[1].split('=')[1]
                if limit == "":
                    limit = "10"
            else:
                limit = "10"
            print("The client has successfully made a request!")

            url = "/drug/label.json?search=openfda.manufacturer_name:" + manufacturer_name + '&' + 'limit=' + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            my_list = []
            a = 0
            start_list = "<head>" + "<h2>" + "These are the manufacturer names'of the drugs that you are looking for:" + '<body style="background-color: #ff99bb">' + "</h2>" + "</head>" "<ol>" + "\n"
            nlimit = int(limit)

            while a < nlimit:
                try:
                    my_list.append(repos['results'][a]["openfda"]['brand_name'][0])
                    a += 1
                except:
                    my_list.append("Not known")
                    print("Drugs produced by this manufacturer are not found")
                    a += 1

            with open("manufacturer_name.html", "w") as f:
                f.write(start_list)
                for element in my_list:
                    list_elements = "<t>" + "<li>" + element
                    f.write(list_elements)


        def list_drugs():   # We use this definition to obatin the default list of drugs
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            info = self.path.strip('label.json?').split('=')
            limit = info[1]
            print("The client has successfully made a request!")

            url = "/drug/label.json?limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            my_list = []
            a = 0
            start_list = "<head>" + "<h2>" + "This is the list of all drugs you are looking for:" + '<body style="background-color: #ff99bb">' + "</h2>" + "</head>" "<ol>" + "\n"
            nlimit = int(limit)

            while a < nlimit:
                try:
                    my_list.append(repos['results'][a]["openfda"]['brand_name'][0])
                    a += 1
                except:
                    my_list.append("Not known")
                    print("This drug doesn't exist in this list")
                    a += 1

            with open("drugs_list.html", "w") as f:
                f.write(start_list)
                for element in my_list:
                    list_elements = "<t>" + "<li>" + element
                    f.write(list_elements)


        def list_manufacturers():   # We use this definition to obtain a default manufacturer
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            info = self.path.strip('label.json?').split('=')
            limit = info[1]
            print("The client has successfully made a request!")

            url = "/drug/label.json?limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            my_list = []
            a = 0
            start_list = "<head>" + "<h2>" + "This is the list of all manufacturers you are looking for:" + '<body style="background-color: #ff99bb">' + "</h2>" + "</head>" "<ol>" + "\n"
            nlimit = int(limit)

            while a < nlimit:
                try:
                    my_list.append(repos['results'][a]["openfda"]['manufacturer_name'][0])
                    a += 1
                except:
                    my_list.append("Not known")
                    print("This manufacturer doesn't exist in this list")
                    a += 1

            with open("manufacturers_list.html", "w") as f:
                f.write(start_list)
                for element in my_list:
                    list_elements = "<t>" + "<li>" + element
                    f.write(list_elements)


        def list_warnings():   # We use this definition to obtain a default list of the grugs' warnings
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            info = self.path.strip('label.json?').split('=')
            limit = info[1]
            print("The client has successfully made a request!")

            url = "/drug/label.json?limit=" + limit
            print(url)

            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            repos_raw = r1.read().decode("utf-8")
            conn.close()
            repos = json.loads(repos_raw)

            my_list = []
            warnings = []
            a = 0
            b = 0
            start_list = "<head>" + "<h2>" + "This is the list of all warnings of the drugs you are looking for:" + '<body style="background-color: #ff99bb">' + "</h2>" + "</head>" "<ol>" + "\n"
            nlimit = int(limit)

            while a < nlimit:
                try:
                    my_list.append(repos['results'][a]["openfda"]['brand_name'][0])
                    a += 1
                except:
                    my_list.append("Not known")
                    a += 1

            while b < nlimit:
                try:
                    warnings.append(repos['results'][a]['warnings'][0])
                    b += 1
                except:
                    warnings.append("Not known")
                    b += 1

            with open("warnings_list.html", "w") as f:
                f.write(start_list)
                i = 0

                while i < nlimit:
                    list_elements = "<t>" + "<li>" + "The warnings for the drug " + my_list[i] + " are " + warnings[i]
                    f.write(list_elements)
                    i += 1


        if self.path == "/":
            try:
                print("SEARCH: The client is searching a web")
                with open("search.html", 'r') as f:
                    message = f.read()
                    self.wfile.write(bytes(message, "utf8"))
            except KeyError:
                print("ERROR")
                print("Not found")
                with open("error.html", "r") as f:
                    message = f.read()
                    self.wfile.write(bytes(message, "utf8"))

        elif 'searchDrug' in self.path:
            active_ingredient()
            with open("data_drugs.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli,"utf8"))

        elif 'searchCompany' in self.path:
            manufacturer_name()
            with open("manufacturer_name.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli, "utf8"))

        elif 'listDrugs' in self.path:
            list_drugs()
            with open("drugs_list.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli, "utf8"))

        elif 'listCompanies' in self.path:
            list_manufacturers()
            with open("manufacturers_list.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli, "utf8"))

        elif 'listWarnings' in self.path:
            list_warnings()
            with open("warnings_list.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli, "utf8"))

        elif 'secret' in self.path:
            with open("secret.html", "r") as f:
                pauli = f.read()
                self.wfile.write(bytes(pauli, "utf8"))

        elif 'redirect' in self.path:
            print("The client wants to go back to the initial web page")
            with open("search.html", 'r') as f:
                mensaje = f.read()
                self.wfile.write(bytes(mensaje, "utf8"))

        else:
            print("ERROR")
            print("Not found")
            with open("error.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))


        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at %s:%s" % (IP, PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print("")
print("Server stopped!")