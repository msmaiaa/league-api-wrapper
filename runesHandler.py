import requests
import asyncio
from handlers import Handler
import json


handler = Handler()

class Rune:
    async def getRunes(self, connection, championId, position):
        await self.getChampion(connection, championId, position)

    async def getChampion(self, connection, championId, position):
        version = await self.getLeagueVersion()
        req = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json').json()

        for c in req["data"].keys():
            chId = int(req['data'][c]['key'])
            if chId == championId:
                scraper = RuneScraper()
                await scraper.handleScrape(connection, req['data'][c]['id'], position)
            
    async def getLeagueVersion(self):
        res = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
        return res[0]

class RuneScraper:
    def __init__(self):
        #sniffed the api xD
        self.url = 'https://app.mobalytics.gg/api/lol/champions/v1/meta?name='

    async def handleScrape(self, connection, champion, position):
        print(f"Getting the best available runes for {champion}")
        self.url = f'{self.url}{champion}'
        r = requests.get(self.url)
        if r.status_code == 200:
            await self.performScrape(connection, r.json(), position, champion)
        else:
            print("Error while trying to get runes")
    
    async def performScrape(self, connection, r, position, champion):
        primaryStyleId = int(r['data']['roles'][0]['builds'][0]['perks']['style'])
        subStyleId = int(r['data']['roles'][0]['builds'][0]['perks']['subStyle'])
        championName = champion
        perks = []
        for i in r['data']['roles'][0]['builds'][0]['perks']['ids']:
            perks.append(int(i))
        fetchRunes = await handler.con(connection, 'get', '/lol-perks/v1/pages')
        runePages = await fetchRunes.json()
        firstPageId = runePages[0]["id"]

        data = {
            "autoModifiedSelections": [0],
            "current": True,
            "id": firstPageId,
            "isActive": True,
            "isDeletable": True,
            "isEditable": True,
            "isValid": True,
            "lastModified": 0,
            "name": championName,
            "order": 0,
            "primaryStyleId": primaryStyleId,
            "selectedPerkIds": perks,
            "subStyleId": subStyleId
        }

        deleted = await handler.con(connection, 'delete', f'/lol-perks/v1/pages/{firstPageId}')
        if deleted.status == 201:
            print("deleted")
        new = await handler.con(connection, 'post', f'/lol-perks/v1/pages', data=data)
        if new.status == 201:
            print("created with success")
            print(new.response)
        
        
