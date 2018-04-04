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

#Obtaining the id, purpose and manufacturer name from one drug
print("The id of the drug is", repos['results'][0]['id'])
print("The purpose of the drig is", repos['results'][0]['purpose'])
print("The manufacturer name is", repos['results'][0]['openfda']['manufacturer_name'])

#Obtaining the id of the first 10 drugs
for elem in repos["results"]:
	print("The id is:", elem["id"])