###############################################################################
#
# Copyright (c) 2017-2020 Master AI, Inc.
# ALL RIGHTS RESERVED
#
# Use of this library, in source or binary form, is prohibited without written
# approval from Master AI, Inc.
#
###############################################################################

"""
Module to interface with your AutoAuto Labs account.

This is a **synchronous** interface.
"""

import os
import time

from auto.asyncio_tools import get_loop
from auto.services.labs.rpc.client_sync import LabsService


def send_message_to_labs(msg):
    """
    Send a message `msg` to your AutoAuto Labs account.
    Return True if the message was sent, else return False.
    """
    client = _global_client()
    to_user_session = os.environ.get('TO_USER_SESSION', None)
    to_username     = os.environ.get('TO_USERNAME', None)
    if to_user_session:
        msg['to_user_session'] = to_user_session
    elif to_username:
        msg['to_username'] = to_username
    did_send = client.send(msg)
    time.sleep(0.1)  # Throttle messages to the Labs servers. Please be nice to our servers, else your account will be suspended.
    return did_send


def receive_message_from_labs(peer_only=True):
    """
    Wait for the next message from the Labs server, then return it.
    If `peer_only` is True, then only messages received from a
    peer devices are returned; else, any next message from the
    server is returned.
    """
    client = _global_client()
    return client.receive(peer_only)


# Alias
send = send_message_to_labs
receive = receive_message_from_labs


def _global_client():
    global _CLIENT
    try:
        _CLIENT
    except NameError:
        _CLIENT = LabsService(get_loop())
        _CLIENT.connect()
    return _CLIENT

