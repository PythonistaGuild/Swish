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

import asyncio

import swish
from swish.app import App
from swish.logging import setup_logging


banner: str = rf"""
                __        _      
              _/  \    _(\(o     
             /     \  /  _  ^^^o 
            /   !   \/  ! '!!!v' 
           !  !  \ _' ( \____    
           ! . \ _!\   \===^\)   
            \ \_!  / __!         
         .   \!   /    \         
       (\_      _/   _\ )        
        \ ^^--^^ __-^ /(__       
         ^^----^^    "^--v'\
----------------------------------------------------------------------         
Swish - The standalone audio player and server for bots on Discord.
Version: {swish.__version__}
----------------------------------------------------------------------
"""
print(banner)


setup_logging()
app: App = App()

loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()


try:
    loop.create_task(app.run())
    loop.run_forever()
except KeyboardInterrupt:
    pass
