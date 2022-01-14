hooks = ["MESSAGE_CREATE"]
def run(event, ctx, bot):
    if ctx["content"].startswith(":") and not(int(ctx["author"]["id"]) in bot.config["authed"]):
        bot.send_msg(ctx["channel_id"], "you lack the proper authentication")
        return
    if ctx["content"] == ":ops":
        bot.send_msg(ctx["channel_id"], ", ".join([str(ident) for ident in bot.config["authed"]]))
    elif ctx["content"].startswith(":op"):
        for mention in ctx["mentions"]:
            bot.config["authed"].append(int(mention["id"]))
            bot.send_msg(ctx["channel_id"], f"added {mention['username']} to the session authed!")
            bot.logger.write(f"added auth {mention['id']} {mention['username']}")