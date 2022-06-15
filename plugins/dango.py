"""
the "hello world" (if you will) of the plugin system.
there are only two required parts:
* 'hooks': a list of dispatch events to run() on
* run(event, ctx, bot): the function to run on-event, where event is the trigger,
    ctx is the 'd'(data) key of the response, and 'bot' is the current bot
    instance.
the rest is up to you.
this particular example listens for a message that contains the string 'dango' and 
    returns a response, similar to the traditional 'hello' -> 'hello, world!'
    test interaction
"""

hooks = ["MESSAGE_CREATE"] # run() will be called when client.dispatch() gets a MESSAGE_CREATE
def run(event, ctx, bot):
        if ctx["content"] == "dango": # if the message body matches...
            bot.api.send_msg(ctx["channel_id"], "to all the motherfuckers that shed a tear")