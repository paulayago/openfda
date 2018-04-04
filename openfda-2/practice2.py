
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#There are only 4 drugs that contain the active ingredient of the aspirin
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=4", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
for i in range (len (repos['results'])):
    aspirin = repos['results'][i]
    if (aspirin['openfda']):
        #In only 2 of the 4 drugs the manufacturer name is specified (inside the openfda) that is why it only prints 2 manufaturer names
        print('Manufacturer: ', aspirin['openfda']['manufacturer_name'][0])
