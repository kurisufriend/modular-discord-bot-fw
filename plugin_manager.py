import os
import sys

class plugin_manager():
    def __init__(self, logger, plugin_path = "./plugins"):
        sys.path.append(plugin_path) # needed to __import__ scripts without a hassle, shouldn't cause an issue
        plugins = [name.split(".py")[0] for name in os.listdir(plugin_path) if name.endswith(".py")]
        self.plugins_loaded = []
        for plugin in plugins:
            module = __import__(plugin)
            if not(hasattr(module, "run")) or not(hasattr(module, "hooks")):
                self.logger.write("plugin {plugin} is invalid: crucial attribute missing!")
            else:
                self.plugins_loaded.append(module)
    def handle(self, event, ctx, bot):
        for plugin in self.plugins_loaded:
            if event in plugin.hooks:
                getattr(plugin, "run")(event, ctx, bot)