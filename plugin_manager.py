import os
import sys

class plugin_manager():
    def __init__(self, logger, plugin_path = "./plugins"):
        sys.path.append(plugin_path) # needed to __import__ scripts without a hassle, shouldn't cause an issue
        plugins = [name.split(".py")[0] for name in os.listdir(plugin_path) if name.endswith(".py")]
        self.plugins_loaded = []
        for plugin in plugins:
            try:
                module = __import__(plugin)
            except: 
                logger.write(f"error loading plugin {plugin}")
                continue
            if not(hasattr(module, "run")) or not(hasattr(module, "hooks")):
                logger.write(f"plugin {plugin} is invalid: crucial attribute missing!")
                continue
            else:
                self.plugins_loaded.append(module)
                logger.write(f"loaded plugin {module.__name__}") # this name will be used for hotloading
    def handle(self, event, ctx, bot):
        for plugin in self.plugins_loaded:
            if event in plugin.hooks:
                try:
                    getattr(plugin, "run")(event, ctx, bot)
                except Exception as e:
                    bot.logger.write(e)