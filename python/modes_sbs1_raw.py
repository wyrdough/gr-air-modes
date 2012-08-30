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
#from datetime import *

class modes_output_sbs1_raw:
  def __init__(self):
    self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._s.bind(('', 30006))
    self._s.listen(1)
    self._s.setblocking(0) #nonblocking
    self._conns = [] #list of active connections

  def __del__(self):
    self._s.close()

  def output(self, msg):
    out = self.format_sbs1(msg)
    for conn in self._conns[:]: #iterate over a copy of the list
      try:
        conn.send(out)
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

  def format_sbs1(self, msg):
    out = ""
    fulltime = "%.9f" % time.time()
    (sec, nsec) = fulltime.split('.')
    ts = long(nsec) % 16777215
   
    hexts = "%06x" % ts 
    hexlist = list(hexts)
    reversehex = "%s%s%s%s%s%s" % (hexlist[4], hexlist[5], hexlist[2], hexlist[3], hexlist[0], hexlist[1])
    ts = reversehex.upper()
   
    (payload, crc, level, notreallyatimestamp) = msg.split(" ") 
 
    out = '$00'
    out += ts
    out += ':'
    out += payload.upper()
    out += ";\n"

    return out
