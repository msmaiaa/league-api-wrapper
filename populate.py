import requests

req = requests.get('http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json').json()

championId = 236

for c in req["data"].keys():
    if int(req['data'][c]['key']) == championId:
        name = req['data'][c]['id']
        print(name)
    #print(f"key: {req['data'][c]['key']} id: {req['data'][c]['id']}")