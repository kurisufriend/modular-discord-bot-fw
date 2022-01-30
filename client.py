import websockets, asyncio, json, sys, requests
from random import randint
import disc_api
from grim_logger import glog, glog_level
from plugin_manager import plugin_manager

class client():
    def __init__(self, config_path = None):
        self.logger = glog(level = glog_level.TRACE)
        self.ws = None
        self.last_sequence = None
        self.session_id = None
        self.user = None
        if not config_path: # this really really really simplifies things even if it is technically messier than a default param itself
            config_path = "config.json"
        self.logger.write(f"loading config from {config_path}")
        with open(config_path, "r") as conf_fd:
            self.config = json.loads(conf_fd.read())
        self.plugman = plugin_manager(self.logger, plugin_path = self.config["plugin_path"])
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
            await self.ws.send(json.dumps({"op":2, "d":{"token":self.config["token"], "intents": 513, "properties":{"$os":"linux", "browser":"mdbf", "device":"mdbf"}}}))
        else:
            # https://discord.com/developers/docs/topics/gateway#identify-example-identify
            await self.ws.send(json.dumps({"op":6, "d":{"token":self.config["token"], "session_id":self.session_id, "seq":self.last_sequence}}))
    async def op_invalid_session(self, res):
        await asyncio.sleep(randint(1, 5)) # try again
        await self.ws.send(json.dumps({"op":2, "d":{"token":self.config["token"], "intents": 513, "properties":{"$os":"linux", "browser":"mdbf", "device":"mdbf"}}}))
    async def op_dispatch(self, res):
        if res["t"] == "READY":
            self.session_id = res["d"]["session_id"]
            self.user = res["d"]["user"]
        self.plugman.handle(res["t"], res["d"], self)
    def run(self):
        asyncio.run(self.shit())
    def send_msg(self, id, message):
        endpoint = f"https://discordapp.com/api/channels/{id}/messages"
        # fstring wasn't working for the auth
        headers = {"Authorization": "Bot {0}".format(self.config["token"]), "User-Agent": "mbdf (cynic.moe, v1)", "Content-Type": "application/json"}
        res = requests.post(endpoint, headers = headers, data = json.dumps({"content": message}))
        self.logger.write(headers)
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass # this should destruct all members probably maybe