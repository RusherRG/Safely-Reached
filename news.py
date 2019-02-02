import requests,pprint

query = "Ruia College"
key = "904b965db90847858db4c17bafd2ea75"
url = "https://newsapi.org/v2/everything?q="+query+"&apiKey="+key
response = requests.get(url)
response = response.json()
pprint.pprint(response)