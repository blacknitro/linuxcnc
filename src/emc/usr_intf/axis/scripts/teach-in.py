#!/usr/bin/python
"""Usage:
    python teach.py nmlfile outputfile
If outputfile is not specified, writes to standard output.

You must ". scripts/emc-environment" before running this script, if you use
run-in-place.
"""
#    Copyright 2007 Jeff Epler <jepler@unpythonic.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import emc
import Tkinter
import sys
import os
linenumber = 1;
print os.getcwd( )

#if len(sys.argv) > 1:
#    emc.nmlfile = sys.argv[1]

if len(sys.argv) > 1:
    outfile = sys.argv[1]
    sys.stdout = open(outfile, 'w')
#else:
#    sys.stdout = open('../Teached.ngc', 'w')

#
#  Output relative config ngc file header for SRX611
#

print "(Generated by Arais Robot Technology: EMC2 teach-in 2010)"
print "(User specific parameters)"
print "#1000 = 84.9814 (X Center)"
print "#1001 = -404.5228 (Y Center)"
print "#1002 = 230 (Z Bottom)"
print "#1003 = -1 (A shift)"
print "#2000 = 266 (X INIT)"
print "#2001 = -426 (Y INIT)"
print "#2002 = 365 (INIT/SAFE Z )"
print "#3000 = 30000 ( Engraving Feedrate )"
print "#3002 = 5000 ( Pathing Feedrate)"
print "#3003 = 180000 ( A homing Feedrate)"
print "F#3002 "
print "G0Y#2001X#2000"
print "G0Z#2002"
print " "
print "(Teached Path)"

s = emc.stat()

def get_cart():
    s.poll()
    position = " ".join(["%-.4f"] * s.axes)
    return position % s.position[:s.axes]
    
def get_joint():
    s.poll()
    position = " ".join(["%-.4f"] * s.axes)
    return position % s.joint_actual_position[:s.axes]

def log():
    p = get_cart()
    label1.configure(text='Learned:  %s' % p)
    print "G1X"+p.split(' ')[0]+"Y"+p.split(' ')[1]+ "Z" + p.split(' ')[2] +"A"+ p.split(' ')[3]

def show():
    s.poll()
    if world.get():
	p = get_cart()
 	p = "X:["+p.split(' ')[0]+"] Y:["+p.split(' ')[1]+"] Z:["+p.split(' ')[2]+"] A:["+p.split(' ')[3]+"]"
    else:
	p = get_joint()
	p = "J0:["+p.split(' ')[0]+"] J1:["+p.split(' ')[1]+"] J2:["+p.split(' ')[2]+"] J3:["+p.split(' ')[3]+"]"
    label2.configure(text='%s' % p)
    
    app.after(100, show)

det = 0
def destory_bind(x):
    global det
    if det == 0:
        print "M2"
    det = 1

app = Tkinter.Tk(); app.wm_title('EMC2 Teach-In')
app.bind('<Destroy>',destory_bind)
world = Tkinter.IntVar(app)

button = Tkinter.Button(app, command=log, text='Learn', font=("helvetica", 14))
button.pack(side='left')

label2 = Tkinter.Label(app, width=60, font='fixed', anchor="w")
label2.pack(side='top')

label1 = Tkinter.Label(app, width=60, font='fixed', text="Learned:  (nothing yet)", anchor="w")
label1.pack(side='top')

r1 = Tkinter.Radiobutton(app, text="Joint", variable=world, value=0)
r1.pack(side='left')
r2 = Tkinter.Radiobutton(app, text="World", variable=world, value=1)
r2.pack(side='left')

show()
app.mainloop()

