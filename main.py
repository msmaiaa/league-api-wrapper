from lcu_driver import Connector
import time
import asyncio

connector = Connector()

async def getChampionSelectStatus(connection):
    teste = await con(connection, 'get','/lol-champ-select/v1/session')
    res = await teste.json()
    #print(res)

async def queueHandler(connection, condition):
    if condition:
        await con(connection, 'post', '/lol-lobby/v1/lobby/custom/start-champ-select')
        print("Accepted queue")
    else:
        print("Refused queue")
        await asyncio.sleep(2)
        await con(connection, 'post', '/lol-lobby/v1/lobby/custom/decline-champ-select')
        

async def con(connection, method, url):
    return await connection.request(method, url)


@connector.ready
async def connect(connection):
    print("started")
    res = await con(connection, 'get', '/lol-summoner/v1/current-summoner')
    resultado = await res.json()
    print(resultado["summonerId"])

@connector.close
async def disconnect(connection):
    print('Finished task')

#eventos
@connector.ws.register('/lol-summoner/v1/current-summoner', event_types=('UPDATE',))
async def icon_changed(connection, event):
    print(f'The summoner {event.data["displayName"]} was updated.')

@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def champion_changed(connection, event):
    print(f"{event.data}")

@connector.ws.register('/lol-lobby/v2/lobby/matchmaking/search-state', event_types=('UPDATE',))
async def search_state(connection, event):
    if event.data["searchState"] == 'Searching':
        print("Searching for match")
    elif event.data["searchState"] == 'Found':
        await queueHandler(connection, False)
        print("Found match")

connector.start()