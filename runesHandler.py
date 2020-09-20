import requests
import asyncio
from handlers import Handler
from bs4 import BeautifulSoup

handler = Handler()


class Rune:
    async def getRunes(self, connection, championId, position):
        await self.getChampion(championId, position)

    async def getChampion(self, championId, position):
        print(championId)
        print(position)
        version = await self.getLeagueVersion()
        req = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json').json()

        for c in req["data"].keys():
            chId = int(req['data'][c]['key'])
            if chId == championId:
                scraper = RuneScraper()
                await scraper.handleScrape(req['data'][c]['id'], position)
                #print(f"{req['data'][c]['key']} {req['data'][c]['id']}")
            
    async def getLeagueVersion(self):
        res = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
        return res[0]

class RuneScraper:
    def __init__(self):
        self.url = 'https://www.op.gg/champion/'

    async def handleScrape(self, champion, position):
        print(f'position: {position} champion: {champion}')
        #print(f"Getting the best available runes for {champion}")
        #self.url = f'{self.url}{champion}/statistics/{position}'
        #r = requests.get(self.url)
        #if r.status_code == 200:
        #    await self.performScrape(r)
        #else:
        #    print("Error while trying to get runes")
    
    async def performScrape(self, r):
        print(r.text[:500])
