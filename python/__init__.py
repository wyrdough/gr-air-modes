#
# Copyright 2008,2009 Free Software Foundation, Inc.
# 
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio gr-air-modes package. It provides a library and
application for receiving Mode S / ADS-B signals from aircraft. Use
uhd_modes.py as the main application for receiving signals. cpr.py
provides an implementation of Compact Position Reporting. altitude.py
implements Gray-coded altitude decoding. Various plugins exist for SQL,
KML, and PlanePlotter-compliant SBS-1 emulation output. mlat.py provides
an experimental implementation of a multilateration solver.
'''

# ----------------------------------------------------------------
# Temporary workaround for ticket:181 (swig+python problem)
import sys
_RTLD_GLOBAL = 0
try:
    from dl import RTLD_GLOBAL as _RTLD_GLOBAL
except ImportError:
    try:
	from DLFCN import RTLD_GLOBAL as _RTLD_GLOBAL
    except ImportError:
	pass
    
if _RTLD_GLOBAL != 0:
    _dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(_dlopenflags|_RTLD_GLOBAL)
# ----------------------------------------------------------------


# import swig generated symbols into the gr-air-modes namespace
from air_modes_swig import *

# import any pure python here
#
from modes_print import modes_output_print
from modes_sql import modes_output_sql
from modes_sbs1 import modes_output_sbs1
from modes_sbs1_raw import modes_output_sbs1_raw
from modes_kml import modes_kml
from modes_raw_server import modes_raw_server
from modes_exceptions import *
#this is try/excepted in case the user doesn't have numpy installed
try:
    from modes_flightgear import modes_flightgear
    from Quaternion import *
except ImportError:
    print "gr-air-modes warning: numpy+scipy not installed, FlightGear interface not supported"
    pass

# ----------------------------------------------------------------
# Tail of workaround
if _RTLD_GLOBAL != 0:
    sys.setdlopenflags(_dlopenflags)      # Restore original flags
# ----------------------------------------------------------------
