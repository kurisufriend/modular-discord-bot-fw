import websockets, asyncio, json
import disc_api
class client():
    def __init__(self):
        pass
    async def shit():
        # https://discord.com/developers/docs/topics/gateway#connecting-to-the-gateway
        # you're supposed to ask an HTTP endpoint what the ws gateway is but the docs didnt tell me the domain after 1sec so HAHA NOPE
        async with websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9") as ws: # they seem to be fond of making new versions randomly and still supporting old ones?
            while True:                                                                     # they may or may not drop support for this soon
                data = (await ws.recv())
                print(data)
                break
    def run():
        asyncio.run(shit())
