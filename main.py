from client import client
from sys import argv, exit

olive = None
if len(argv) < 2:
    olive = client() # is this clean? who knows!
else:
    olive = client(config_path = argv[1])
olive.run()