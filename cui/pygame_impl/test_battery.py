###############################################################################
#
# Copyright (c) 2017-2018 AutoAuto, LLC
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from AutoAuto, LLC.
#
###############################################################################

import time

from cui.pygame_impl import CuiPyGame


if __name__ == '__main__':
    c = CuiPyGame()
    c.init()

    for i in range(0, 101):
        c.set_battery_percent(i)
        time.sleep(0.01)
    for i in range(100, -1, -1):
        c.set_battery_percent(i)
        time.sleep(0.01)

