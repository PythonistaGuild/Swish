from __future__ import annotations

# stdlib
import asyncio

# local
from src import Server, logging


logging.setup()


BANNER = """
######################################################
##   (`-').->     .->     _      (`-').-> (`-').->  ##
##   ( OO)_   (`(`-')/`) (_)     ( OO)_   (OO )__   ##
##  (_)--\_) ,-`( OO).', ,-(`-')(_)--\_) ,--. ,'-'  ##
##  /    _ / |  |\  |  | | ( OO)/    _ / |  | |  |  ##
##  \_..`--. |  | '.|  | |  |  )\_..`--. |  `-'  |  ##
##  .-._)   \|  |.'.|  |(|  |_/ .-._)   \|  .-.  |  ##
##  \       /|   ,'.   | |  |'->\       /|  | |  |  ##
##   `-----' `--'   '--' `--'    `-----' `--' `--'  ##
## VERSION: 0.0.1a - BUILD: N/A                     ##
###################################################### 
"""
print(BANNER)


loop = asyncio.new_event_loop()
app = Server()


try:
    loop.create_task(app._run_app())
    loop.run_forever()
except KeyboardInterrupt:
    pass
