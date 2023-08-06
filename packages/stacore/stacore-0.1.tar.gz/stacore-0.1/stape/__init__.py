# stape
# Streaming telemetry analytics for power engineers.
#
# Author:   Benjamin Bengfort <benjamin@pingthings.io>
# Created:  Mon Dec 17 20:59:00 2018 -0500
#
# Copyright (C) 2018 Ping Things
# For license information, see LICENSE.txt
#
# ID: stape.py [] benjamin@bengfort.com $

"""
Streaming telemetry analytics for power engineers.
"""

##########################################################################
## Imports
##########################################################################

# Import the version number at the top level
from .version import get_version, __version_info__


##########################################################################
## Package Version
##########################################################################

__version__ = get_version(short=True)