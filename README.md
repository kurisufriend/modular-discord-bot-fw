# modular-discord-bot-fw
framework for discord bots that uses contained files for individual feature plugins that can be modified and reloaded on the fly

basic structure:
* client class has implementations for handling opcodes
    * event response is up to the client (!!)
    * this lets us expose events for plugins to hook into, but keeps core API interaction defined in-class
    * any and all bot features should be useable via independent feature plugins
        * these are dynamically found and run, so they can be hotloaded, modified, etc. without disconnecting or restarting the whole bot session

todo before it's basically finished:
* basic rate limiting
* ~~plugin manager & hook integration~~
* make sure broken sockets are properly addressed with a resume or reconnect
* ~~default plugins so the bot does _something_ out of the box~~
    * ~~plugin reloading, user (command) authentication, etc. will also probably be written in plugin form~~
* initial presence in config
* take config as cli param
* save session config to file