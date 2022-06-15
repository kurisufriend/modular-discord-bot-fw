import requests, json

gateway_opcodes = { # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
    0: "dispatch",
    1: "heartbeat",
    2: "identify",
    3: "presence_update",
    4: "voice_state_update",
    6: "resume",
    7: "reconnect",
    8: "request_guild_members",
    9: "invalid_session",
    10: "hello",
    11: "heartbeat_ack"
}
gateway_close_event_codes = { # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-close-event-codes
    4000: "We're not sure what went wrong. Try reconnecting?",
    4001: "You sent an invalid Gateway opcode or an invalid payload for an opcode. Don't do that!",
    4002: "You sent an invalid payload to us. Don't do that!",
    4003: "You sent us a payload prior to identifying.",
    4004: "The account token sent with your identify payload is incorrect.",
    4005: "You sent more than one identify payload. Don't do that!",
    4007: "The sequence sent when resuming the session was invalid. Reconnect and start a new session.",
    4008: "Woah nelly! You're sending payloads to us too quickly. Slow it down! You will be disconnected on receiving this.",
    4009: "Your session timed out. Reconnect and start a new one.",
    4010: "You sent us an invalid shard when identifying.",
    4011: "The session would have handled too many guilds - you are required to shard your connection in order to connect.",
    4012: "You sent an invalid version for the gateway.",
    4013: "You sent an invalid intent for a Gateway Intent. You may have incorrectly calculated the bitwise value.",
    4014: "You sent a disallowed intent for a Gateway Intent. You may have tried to specify an intent that you have not enabled or are not approved for."
}

class rest():
    def __init__(self, gatewa, header):
        self.gateway = gatewa
        self.headers = header
    def get(self, endpoint):
        return requests.get(self.gateway+endpoint, headers = self.headers).text
    def post(self, endpoint, dat):
        requests.post(self.gateway+endpoint, headers = self.headers, data = dat)


    def get_channel(self, id):
        return self.get(f"/channels/{id}")
    def get_guild_channels(self, id):
        return self.get(f"/guilds/{id}/channels")
    
    def execute_webhook(self, link, message, name):
        self.post(link, json.dumps({"content": message, "username": name}))
    def send_msg(self, id, message):
        self.post(f"/channels/{id}/messages", json.dumps({"content": message}))