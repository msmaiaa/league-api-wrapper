import requests
import asyncio
from handlers import Handler


handler = Handler()


class Rune:
    async def getRunes(self, connection, championId, position):
        await self.getChampion(championId, position)

    async def getChampion(self, championId, position):
        version = await self.getLeagueVersion()
        req = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json').json()

        for c in req["data"].keys():
            chId = int(req['data'][c]['key'])
            if chId == championId:
                scraper = RuneScraper()
                await scraper.handleScrape(req['data'][c]['id'], position)
            
    async def getLeagueVersion(self):
        res = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
        return res[0]

class RuneScraper:
    def __init__(self):
        #sniffed the api xD
        self.url = 'https://app.mobalytics.gg/api/lol/champions/v1/meta?name='

    async def handleScrape(self, champion, position):
        print(f"Getting the best available runes for {champion}")
        self.url = f'{self.url}{champion}'
        r = requests.get(self.url)
        if r.status_code == 200:
            await self.performScrape(r.json())
        else:
            print("Error while trying to get runes")
    
    async def performScrape(self, r):
        for r in r["data"]["roles"]:
            print(r["value"])
        

class Debug:
    async def test(self):
        scraper = RuneScraper()
        await scraper.handleScrape('Ahri', ' ')

async def main():
    debugger = Debug()
    await debugger.test()

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())