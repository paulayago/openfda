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
    # Create the first function that will return the main html page when the progam is executed
    def return_html(self):
        #The file "search.html" is already being created and stored inside the same directory
        with open("search.html", 'r') as f:
            message = f.read()
            #The content is returned
            return message

    #The second function is defined, it recieves a list of information and generates an html file
    def return_web (self, list):
        #The information is obtained and transformed into and html
        html_list = """
                                <html>
                                    <head>
                                        <title>OpenFDA </title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        #Iterates over each element
        for i in list:
            html_list += "<li>" + i + "</li>"
        #Closes the html file
        html_list += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return html_list

    # The third function is created which calls for the server where we are going to obtain all the information needed
    def obtain_results(self, limit=10):
        #Calls for the server
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json" + "?limit=" + str(limit))
        print("/drug/label.json" + "?limit=" + str(limit))
        #Obtains a response from the server
        r1 = conn.getresponse()
        data1 = r1.read().decode("utf8")
        data = json.loads(data1)
        results = data['results']
        return results

    #This last function is the one that integrates all the other ones defined above
    def do_GET(self):
        #This variable contains the information in the search path, it separates them by the "?" in order to obtain
        #two elements each one with a different position,
        search_resource = self.path.split("?")

        #Now, we want the information contained in the second element, that corresponds to the one that followed the "?"
        if len(search_resource) > 1:
            parameter = search_resource[1]
        else:
            parameter = ""
        limit = 1

        # Obtain the arguments
        if parameter:
            #The parameter we have already isolated contains two arguments, we separate them by the "="
            parse_limit = parameter.split("=")
            #Obtain the limit argument
            if parse_limit[0] == "limit":
                #The second position is an int
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("No parameters")

        if self.path=='/':
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #Call the first function we have defined, creates a web that contains the html
            html=self.return_html()
            # Write content as utf-8 data
            self.wfile.write(bytes(html, "utf8"))

        #Now if we want to search for a drug:
        elif 'searchDrug' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            #Isolate the information that provides us the drug
            drug=self.path.split('=')[1]

            #Empty list that will later contain all the information in relation to the first drug (the one searched)
            #This information is the one that iterates over and over in the for loop
            drugs = []

            # Calls for the server
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit="+str(limit) + '&search=active_ingredient:' + drug)
            # Obtains a response from the server
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            #Now we are searching inside the library
            information_data = json.loads(data)
            search_drug = information_data['results']
            for results in search_drug:
                if ('generic_name' in results['openfda']):
                    #Adding the information the list prevoiusly created
                    drugs.append(results['openfda']['generic_name'][0])
                #In case it doesn´t appear
                else:
                    drugs.append('Unknown')
            #All the results obtain are return as a web, calling the function already created
            final_html = self.return_web(drugs)
            #Return in an html file
            self.wfile.write(bytes(final_html, "utf8"))

        #Searching for a company:
        elif 'searchCompany' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            #All the steps are the same as in the previous case
            company=self.path.split('=')[1]
            companies = []

            # Calls for the server
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:'+ company)
            # Obtains a response from the server
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            information_data = json.loads(data)
            search_company = information_data['results']

            for event in search_company:
                #In this case it is not necessary to search inside the "openfda" tab
                companies.append(event['openfda']['manufacturer_name'][0])
            #Returns the information in html as well as before
            final_html = self.return_web(companies)
            self.wfile.write(bytes(final_html, "utf8"))

        #To obtain the list of drugs
        elif 'listDrugs' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drugs = []
            #As we need to know the number of drugs the client wants to be display on the screen, we need to isolate
            #that value from the saerch path, if not, it would always return only 1 drug, as the limit is defined above
            if len(self.path.split("?")) > 1:
                limit = self.path.split("?")[1].split("=")[1]
            results = self.obtain_results(limit)
            for element in results:
                if ('generic_name' in element['openfda']):
                    drugs.append (element['openfda']['generic_name'][0])
                else:
                    drugs.append('Unknown')
            final_html = self.return_web (drugs)
            self.wfile.write(bytes(final_html, "utf8"))

        #To obtain the list of companies
        elif 'listCompanies' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            if len(self.path.split("?")) > 1:
                limit = self.path.split("?")[1].split("=")[1]
            results = self.obtain_results (limit)
            for element in results:
                if ('manufacturer_name' in element['openfda']):
                    companies.append (element['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Unknown')
            final_html = self.return_web(companies)
            self.wfile.write(bytes(final_html, "utf8"))

        #Extension I: List Limits and Drug Warnings
        elif 'listWarnings' in self.path:
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            if len(self.path.split("?")) > 1:
                limit = self.path.split("?")[1].split("=")[1]
            results = self.obtain_results (limit)
            for element in results:
                if ('warnings' in element):
                    warnings.append (element['warnings'][0])
                else:
                    warnings.append('Unknown')
            final_html = self.return_web(warnings)
            self.wfile.write(bytes(final_html, "utf8"))

        #Extension IV: Redirect and Authentication
        elif 'redirect' in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        #Extension II: Implement 404, Not found
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
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