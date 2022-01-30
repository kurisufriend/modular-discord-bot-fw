from client import client
from sys import argv, exit

path = None
with client(config_path = None if (len(argv) < 2) else argv[1]) as c:
    c.run()
