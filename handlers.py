import asyncio

class Handler:

    async def con(self, connection, method, url):
        return await connection.request(method, url)

    async def queueHandler(self,connection, condition):
        #decline or accept match
        if condition:
            await self.con(connection, 'post', '/lol-matchmaking/v1/ready-check/accept')
            print("Accepted queue")
        else:
            print("Refused queue")
            await asyncio.sleep(2)
            await self.con(connection, 'post', '/lol-matchmaking/v1/ready-check/decline')
