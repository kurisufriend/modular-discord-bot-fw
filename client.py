import websockets, asyncio, json
from random import randint
import disc_api
from grim_logger import glog, glog_level
class client():
    def __init__(self, token):
        self.logger = glog(level = glog_level.TRACE)
        self.ws = None
        self.last_sequence = None
        self.session_id = None
        self.token = token
        self.user = None
    async def shit(self):
        # https://discord.com/developers/docs/topics/gateway#connecting-to-the-gateway
        # you're supposed to ask an HTTP endpoint what the ws gateway is but the docs didnt tell me the domain after 1sec so HAHA NOPE
        async with websockets.connect("wss://gateway.discord.gg/?encoding=json&v=9") as self.ws:# they seem to be fond of making new versions randomly and still supporting old ones?
            while True:                                                                         # they may or may not drop support for this soon # nevermind we're on v9 now
                data = json.loads(await self.ws.recv())
                handler = getattr(self, "op_"+disc_api.gateway_opcodes[data["op"]], None)
                self.logger.write(data)
                self.last_sequence = data["s"]
                if handler:
                    await handler(data)
    async def heartbeat(self, interval):
        while True:
            self.logger.write(interval/1000)
            await self.ws.send(json.dumps({"op":1, "d":self.last_sequence}))
            await asyncio.sleep(interval/1000)
            self.logger.write("sent heartbeat")
    async def op_hello(self, res):
        if not(self.last_sequence and self.session_id):
            interval = res["d"]["heartbeat_interval"]
            asyncio.get_event_loop().create_task(self.heartbeat(interval))
            await asyncio.sleep(1)
            # https://discord.com/developers/docs/topics/gateway#identify-example-identify
            await self.ws.send(json.dumps({"op":2, "d":{"token":self.token, "intents": 513, "properties":{"$os":"linux", "browser":"mdbf", "device":"mdbf"}}}))
        else:
            # https://discord.com/developers/docs/topics/gateway#identify-example-identify
            await self.ws.send(json.dumps({"op":6, "d":{"token":self.token, "session_id":self.session_id, "seq":self.last_sequence}}))
    async def op_invalid_session(self, res):
        await asyncio.sleep(randint(1, 5)) # try again
        await self.ws.send(json.dumps({"op":2, "d":{"token":self.token, "intents": 513, "properties":{"$os":"linux", "browser":"mdbf", "device":"mdbf"}}}))
    async def op_dispatch(self, res):
        if res["t"] == "READY":
            self.session_id = res["d"]["session_id"]
            self.user = res["d"]["user"]
    def run(self):
        asyncio.run(self.shit())