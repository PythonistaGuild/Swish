import asyncio
import logging

import src


logger = logging.getLogger('swish')
logger.setLevel(logging.DEBUG)
logger.addHandler(src.STDOUT_LOGGER())


print(f"""
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
""")


loop = asyncio.new_event_loop()
app = src.Server()

try:
    loop.create_task(app._run_app())
    loop.run_forever()
except KeyboardInterrupt:
    pass
