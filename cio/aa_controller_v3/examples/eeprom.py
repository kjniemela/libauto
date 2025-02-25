###############################################################################
#
# Copyright (c) 2017-2020 Master AI, Inc.
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from Master AI, Inc.
#
###############################################################################

import asyncio
from pprint import pprint

import cio.aa_controller_v3 as controller

from cio.aa_controller_v3.capabilities import eeprom_store, eeprom_query


async def run():
    c = controller.CioRoot()
    caps = await c.init()
    pprint(caps)

    fd = c.ctlr_fd

    buf = await eeprom_query(fd, 0xA0, 4)
    print(buf)

    await eeprom_store(fd, 0xA0, b'0000')

    buf = await eeprom_query(fd, 0xA0, 4)
    print(buf)
    assert buf == b'0000'

    await eeprom_store(fd, 0xA0, b'1234')

    buf = await eeprom_query(fd, 0xA1, 3)
    print(buf)
    assert buf == b'234'

    buf = await eeprom_query(fd, 0xA2, 2)
    print(buf)
    assert buf == b'34'

    buf = await eeprom_query(fd, 0xA3, 1)
    print(buf)
    assert buf == b'4'

    buf = await eeprom_query(fd, 0xA0, 4)
    print(buf)
    assert buf == b'1234'

    buf = await eeprom_query(fd, 0x0F, 5)
    print(buf)

    await eeprom_store(fd, 0x0F, b'12345')

    buf = await eeprom_query(fd, 0x10, 4)
    print(buf)
    assert buf == b'2345'

    buf = await eeprom_query(fd, 0x11, 3)
    print(buf)
    assert buf == b'345'

    buf = await eeprom_query(fd, 0x12, 2)
    print(buf)
    assert buf == b'45'

    buf = await eeprom_query(fd, 0x13, 1)
    print(buf)
    assert buf == b'5'

    buf = await eeprom_query(fd, 0x0F, 5)
    print(buf)
    assert buf == b'12345'


if __name__ == '__main__':
    asyncio.run(run())

