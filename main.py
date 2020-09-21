from lcu_driver import Connector
from handlers import Handler
from runesHandler import RuneScraper, Rune
import time
import asyncio

connector = Connector()
handler = Handler()
runes = Rune()


async def getId(connection):
    res = await handler.con(connection, 'get', '/lol-summoner/v1/current-summoner')
    resultado = await res.json()
    return resultado["summonerId"]

@connector.ready
async def connect(connection):
    res = await handler.con(connection, 'get', '/lol-summoner/v1/current-summoner')
    resultado = await res.json()
    print(f"Summoner {resultado['displayName']} logged in")

@connector.close
async def disconnect(connection):
    print('Finished task')

#events
@connector.ws.register('/lol-summoner/v1/current-summoner', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'The summoner {event.data["displayName"]} was updated.')
    print(event.data["summonerId"])

@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def champion_changed(connection, event):
    summonerId = await getId(connection)
    for i in event.data["myTeam"]:
        if i["summonerId"] == summonerId:
            #print(i["championId"])
            if i != 0:
                await runes.getRunes(connection, i["championId"], i["assignedPosition"])
    

@connector.ws.register('/lol-lobby/v2/lobby/matchmaking/search-state', event_types=('UPDATE',))
async def search_state(connection, event):
    if event.data["searchState"] == 'Searching':
        print("Searching for match")
    elif event.data["searchState"] == 'Found':
        print("Found match")
        await handler.queueHandler(connection, True)

connector.start()