"""Swish. A standalone audio player and server for bots on Discord.

Copyright (C) 2022 PythonistaGuild <https://github.com/PythonistaGuild>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import annotations


banner: str = """
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
print(banner)


import asyncio
loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()


from swish.logging import setup_logging
setup_logging()


from swish.app import App
app: App = App()


try:
    loop.create_task(app.run())
    loop.run_forever()
except KeyboardInterrupt:
    pass
