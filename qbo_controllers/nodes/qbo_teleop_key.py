#!/usr/bin/env python

# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Willow Garage, Inc. nor the names of its
#      contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from os import system
import curses

import roslib; roslib.load_manifest('qbo_controllers')
import rospy

from geometry_msgs.msg import Twist

def mymain(screen):
    rospy.init_node('QBO_teleop')
    rospy.sleep(0.0001)

    tpub = rospy.Publisher("cmd_vel", Twist)

    a_scale = rospy.get_param("~scale_angular", 1.5)
    l_scale = rospy.get_param("~scale_linear", 0.5)

    t = Twist()
    screen.nodelay(1)
    down = False
    menu(screen, t)
    fnmap = { curses.KEY_LEFT : (1, 0.0),
              curses.KEY_RIGHT : (-1, 0.0),
              curses.KEY_UP : (0.0, 1),
              curses.KEY_DOWN : (0.0, -1)
              }

    while True:
        gotch = screen.getch()
        
        if gotch == 27 or gotch == ord('q') or gotch == ord('Q'): # ESC key or q
            return
        if gotch in fnmap:
            down = True
            ang, lin = fnmap[gotch]
            t.angular.z = ang * a_scale
            t.linear.x = lin * l_scale
            tpub.publish(t)
            menu(screen, t)

def menu(s, twist):
    s.clear()
    s.border(0)
    s.addstr(2, 2, "QBO Control", curses.A_BOLD)
    s.addstr(4, 2, "Use arrow keys to move, ESC or Q to exit", curses.A_BOLD)

    s.addstr(6, 2, "Last Published", curses.A_UNDERLINE)
    s.addstr(7, 2, "Linear:  %1.2f" % twist.linear.x)
    s.addstr(8, 2, "Angular: %1.2f" % twist.angular.z)
    s.refresh()

curses.wrapper(mymain)
