#
# Copyright 2010 Nick Foster
# 
# This file is part of gr-air-modes
# 
# gr-air-modes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# gr-air-modes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with gr-air-modes; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 


import time, os, sys, socket
from string import split, join
from datetime import *
import time
import modes_parse
from modes_exceptions import *

class modes_beast_binary:
  def __init__(self):
    self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._s.bind(('', 9989))
    self._s.listen(1)
    self._s.setblocking(0) #nonblocking
    self._conns = [] #list of active connections

  def __del__(self):
    self._s.close()

#  def bin(s):
#    return str(s) if s <= 1 else bin(s>>1) + str(s&1)

  def HexToByte(self, hexStr):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case    
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
      bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
    return ''.join( bytes )

  def parse(self, message):
    # Get a current timestamp. Hopefully in the future we'll have a real one even on rtl_sdr devices
    now = "%.9f" % time.time()
    [secs, fracs] = now.split('.')
    fakestamp = "%012x" % long(secs[:-5]+fracs)

    #Parse it for type so we can output the correct message type
    [rawdata, ecc, reference, timestamp] = message.split()

    data = modes_parse.modes_reply(long(rawdata, 16))
    ecc = long(ecc, 16)
    msgtype = data["df"]

    signal = "%02x" % int(round(float(reference) * 255))

    if msgtype == 17:
      # Long
      hexout = "1a33"
    else:
      # We don't deal in mode a/c (yet?), so we can ignore the third possibility
      # Short
      hexout = "1a32"

    hexout += fakestamp
    hexout += signal
    hexout += rawdata
      
    return self.HexToByte(hexout)

  def output(self, msg):
    outmsg = self.parse(msg)
    if outmsg is not None:
      for conn in self._conns[:]: #iterate over a copy of the list
        try:
          conn.send(outmsg)
        except socket.error:
          self._conns.remove(conn)
          print "Connections: ", len(self._conns)

  def add_pending_conns(self):
    try:
      conn, addr = self._s.accept()
      self._conns.append(conn)
      print "Connections: ", len(self._conns)
    except socket.error:
      pass
