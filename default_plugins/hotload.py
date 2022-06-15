from importlib import reload
hooks = ["MESSAGE_CREATE"]
def run(event, ctx, bot):
    if ctx["content"].startswith(":") and not(int(ctx["author"]["id"]) in bot.config["authed"]):
        bot.api.send_msg(ctx["channel_id"], "you lack the proper authentication")
        return
    plugin_manager = bot.plugman
    if ctx["content"].startswith(":reload"):
        cmd = ctx["content"].split(" ")[1]
        if not(cmd in [m.__name__ for m in plugin_manager.plugins_loaded]):
            bot.api.send_msg(ctx["channel_id"], f"plugin {cmd} could not be found for reloading!")
        else:
            for m in plugin_manager.plugins_loaded:
                if m.__name__ == cmd:
                    reload(m)
            bot.api.send_msg(ctx["channel_id"], f"reloaded plugin {cmd}!")
            bot.logger.write(f"reloaded {cmd}")
    elif ctx["content"] ==":plugins":
        plugins = ", ".join([m.__name__ for m in plugin_manager.plugins_loaded])
        bot.api.send_msg(ctx["channel_id"], f"{plugins}")