import os
import sys
import threading
class plugin_manager():
    def __init__(self, logger, plugin_path = "./plugins"):
        self.logger = logger
        self.plugins_loaded = []
        self.load_folder("./default_plugins")
        self.load_folder(plugin_path)
    def load_folder(self, path):
        sys.path.append(path) # needed to __import__ scripts without a hassle, shouldn't cause an issue
        plugins = [name.split(".py")[0] for name in os.listdir(path) if name.endswith(".py")]
        for plugin in plugins:
            try:
                module = __import__(plugin)
            except: 
                self.logger.write(f"error loading plugin {plugin}")
                continue
            if not(hasattr(module, "run")) or not(hasattr(module, "hooks")):
                self.logger.write(f"plugin {plugin} is invalid: crucial attribute missing!")
                continue
            else:
                self.plugins_loaded.append(module)
                self.logger.write(f"loaded plugin {module.__name__}") # this name will be used for hotloading
    def handle(self, event, ctx, bot):
        for plugin in self.plugins_loaded:
            if event in plugin.hooks:
                try:
                    threading.Thread(target=getattr(plugin, "run"), args=(event, ctx, bot), daemon=True).start()
                except Exception as e:
                    bot.logger.write(e)
    def __del__(self):
        for plugin in self.plugins_loaded:
            if hasattr(plugin, "clean"):
                getattr(plugin, "clean")()