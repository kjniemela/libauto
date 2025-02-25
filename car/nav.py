###############################################################################
#
# Copyright (c) 2017-2022 Master AI, Inc.
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from Master AI, Inc.
#
###############################################################################

"""
This module connects to the car's controller via the CIO interface.

For beginners, it provides easy functions for navigation for the virtual
car.
"""

from auto.capabilities import list_caps, acquire
from auto.asyncio_tools import thread_safe
from auto.sleep import _physics_client
from .motors import set_steering
from auto import IS_VIRTUAL
import math


def drive_to(target_x, target_z, halt_threshold=2.5):
    """
    Use the car's GPS and Compass to drive the car to the given (x, z) location.

    Works for virtual cars only!
    """
    if not IS_VIRTUAL:
        raise NotImplemented('This function only work on virtual cars.')

    gps = _get_gps()
    compass = _get_compass()
    physics = _physics_client()

    halt_threshold_sqrd = halt_threshold * halt_threshold

    while True:
        x, y, z = gps.query()
        theta = compass.query()

        dx = target_x - x
        dz = target_z - z

        if dx*dx + dz*dz < halt_threshold_sqrd:
            break

        theta *= math.pi / 180.0   # convert degrees to radians
        theta_target = math.atan2(dx, dz)
        theta_diff = theta_target - theta
        theta_diff = math.atan2(math.sin(theta_diff), math.cos(theta_diff))  # normalize into [-pi, +pi]
        steering_angle = theta_diff * 180.0 / math.pi

        set_steering(steering_angle)

        # All calls above are non-blocking, but there's no need to loop
        # until we have new data from the physics engine, so below block
        # until the next "tick" of the physics engine, and after that it
        # makes sense to loop back and recompute.
        physics.wait_tick()

    set_steering(0.0)


def drive_route(xz_checkpoints, halt_threshold=2.5):
    """
    Go to each point in the list `xz_checkpoints`.

    Works for virtual cars only!
    """
    for x, z in xz_checkpoints:
        drive_to(x, z, halt_threshold)


@thread_safe
def _get_gps():
    global _GPS
    try:
        _GPS
    except NameError:
        caps = list_caps()
        if 'GPS' not in caps:
            raise AttributeError('This device has no GPS.')
        _GPS = acquire('GPS')
    return _GPS


@thread_safe
def _get_compass():
    global _COMPASS
    try:
        _COMPASS
    except NameError:
        caps = list_caps()
        if 'Compass' not in caps:
            raise AttributeError('This device has no Compass.')
        _COMPASS = acquire('Compass')
    return _COMPASS

