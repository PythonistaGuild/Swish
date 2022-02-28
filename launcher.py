from __future__ import annotations

# stdlib
import asyncio

# local
from src import App, setup_logging


setup_logging()


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
app = App()


try:
    loop.create_task(app._run_app())
    loop.run_forever()
except KeyboardInterrupt:
    pass
