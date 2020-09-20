import requests

req = requests.get('http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json').json()

print(len(req["data"]))
print(req["data"].keys())

for c in req["data"].keys():
    print(f"{req['data'][c]['key']} {req['data'][c]['id']}")