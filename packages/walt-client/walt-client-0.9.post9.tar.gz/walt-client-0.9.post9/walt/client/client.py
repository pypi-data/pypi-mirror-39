#!/usr/bin/env python
"""
WalT (wireless testbed) control tool.
"""
import sys, socket
from walt.client.myhelp import WalTHelp
from walt.client.log import WalTLog
from walt.client.advanced import WalTAdvanced
from walt.client.node import WalTNode
from walt.client.device import WalTDevice
from walt.client.image import WalTImage
from walt.client.startup import init_config
from walt.common.apilink import LinkException
from walt.client.update import client_update
from walt.client.tools import restart
from walt.client.logo import try_add_logo
from walt.client.application import WalTToolboxApplication

WALT_COMMAND_HELP_PREFIX = '''\

WalT platform control tool.

Usage:
    walt CATEGORY SUBCOMMAND [args...]

Help about a given category or subcommand:
    walt CATEGORY --help
    walt CATEGORY SUBCOMMAND --help

Help about WalT in general:
    walt help show

Categories:
'''

class WalT(WalTToolboxApplication):
    """WalT platform control tool."""
    def get_help_prefix(self):
        return try_add_logo(WALT_COMMAND_HELP_PREFIX)

WalT.subcommand("help", WalTHelp)
WalT.subcommand("advanced", WalTAdvanced)
WalT.subcommand("device", WalTDevice)
WalT.subcommand("image", WalTImage)
WalT.subcommand("log", WalTLog)
WalT.subcommand("node", WalTNode)

def run():
    try:
        init_config()
        if client_update():
            restart()   # this will never return, no need to exit
        WalT.run()
    except socket.error:
        print 'Network connection to WalT server failed!'
    except LinkException:
        print 'Issue occured while communicating with WalT server!'
    except KeyboardInterrupt:
        print
        print 'Aborted.'

