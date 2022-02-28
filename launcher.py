from __future__ import annotations


import asyncio
loop = asyncio.new_event_loop()


from src.logging import setup_logging
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
## VERSION: 0.0.1alpha0 - BUILD: N/A                ##
###################################################### 
"""
print(BANNER)


from src.app import App
app = App()


try:
    loop.create_task(app._run_app())
    loop.run_forever()
except KeyboardInterrupt:
    pass
