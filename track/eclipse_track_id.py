#!/usr/bin/env python
#########################################
#   Title: Lunar Track                  #
# Project: Lunar Tracking Program
#    Date: Aug 2016                     #
#  Author: Zach Leffke, KJ4QLP          #
#########################################

import math
import string
import time
import sys
import csv
import os
import ephem

from optparse import OptionParser
from datetime import datetime as dt
from datetime import timedelta
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.interpolate import *
#from mpl_toolkits.basemap import Basemap


deg2rad = math.pi / 180
rad2deg = 180 / math.pi
c       = float(299792458)    #[m/s], speed of light
au2m    = 149597870700

def Circle_Overlap(r,R,d):
    result = 0
    #ref: http://mathworld.wolfram.com/Circle-CircleIntersection.html (eq 13)
    try:
        A = r**2 * math.acos((d**2+r**2-R**2)/(2*d*r))
        B = R**2 * math.acos((d**2+R**2-r**2)/(2*d*R))
        C = 0.5 * math.sqrt((-1*d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))
        result = A + B - C
    except:
        pass
    return result

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def dms_to_dec(DMS):
    data = str(DMS).split(":")
    degrees = float(data[0])
    minutes = float(data[1])
    seconds = float(data[2])
    if degrees < 0 : DEC = -(seconds/3600) - (minutes/60) + degrees
    else: DEC = (seconds/3600) + (minutes/60) + degrees
    return DEC

if __name__ == '__main__':
    #--------START Command Line option parser------------------------------------------------------
    usage  = "usage: %prog "
    parser = OptionParser(usage = usage)
    h_gs_id     = "Ground Station ID [default=%default]"
    h_gs_lat    = "Ground Station Latitude [default=%default]"
    h_gs_lon    = "Ground Station Longitude [default=%default]"
    h_gs_alt    = "Ground Station Altitude [default=%default]"

    #parser.add_option("", "--gs_id" , dest = "gs_id" , action = "store", type = "string",default='VTGS'      , help = h_gs_id)
    #parser.add_option("", "--gs_lat", dest = "gs_lat", action = "store", type = "float", default='37.229977' , help = h_gs_lat)
    #parser.add_option("", "--gs_lon", dest = "gs_lon", action = "store", type = "float", default='-80.439626', help = h_gs_lon)
    #parser.add_option("", "--gs_alt", dest = "gs_alt", action = "store", type = "float", default='610'       , help = h_gs_alt)
    parser.add_option("", "--gs_id" , dest = "gs_id" , action = "store", type = "string",default='MOSCOW_ID' , help = h_gs_id)
    parser.add_option("", "--gs_lat", dest = "gs_lat", action = "store", type = "float", default='46.718971' , help = h_gs_lat)
    parser.add_option("", "--gs_lon", dest = "gs_lon", action = "store", type = "float", default='-116.983578', help = h_gs_lon)
    parser.add_option("", "--gs_alt", dest = "gs_alt", action = "store", type = "float", default='786'       , help = h_gs_alt)
    (options, args) = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------    

    os.system('reset')
    #--Setup Ground Station------------
    gs = ephem.Observer()
    gs.lat, gs.lon, gs.elevation = options.gs_lat*deg2rad, options.gs_lon*deg2rad, options.gs_alt
    #--Setup Solar System Bodies------
    m = ephem.Moon()
    s = ephem.Sun()
    

    while 1:
        d = dt.utcnow()# + timedelta(hours=5.25)
        gs.date = d
        m.compute(gs)
        s.compute(gs)
        os.system('clear')
        solar_az = dms_to_dec(s.az)
        lunar_az = dms_to_dec(m.az)
        delta_az = solar_az - lunar_az
        solar_el = dms_to_dec(s.alt)
        lunar_el = dms_to_dec(m.alt)
        delta_el = solar_el - lunar_el
        separation = math.sqrt(delta_az**2 + delta_el**2)
        solar_dia = dms_to_dec(s.radius) * 2
        lunar_dia = dms_to_dec(m.radius) * 2
        delta_dia = solar_dia - lunar_dia
        eclipse_condition = lunar_dia/2.0 + solar_dia/2.0
        solar_r = s.earth_distance * au2m / 1000
        lunar_r = m.earth_distance * au2m / 1000
        lunar_pd = m.earth_distance * au2m / c
        solar_pd = s.earth_distance * au2m / c
        hor_lo = ""
        hor_hi = ""
        for i in range(57): hor_hi  += unichr(713)
        for i in range(57): hor_lo  += unichr(717)
        print "Time [UTC]: {:s}".format(str(d))
        print "Ground Station ID: {:s}".format(options.gs_id)
        print hor_lo
        az_line = ""
        print color.UNDERLINE + "|                  | Lunar     | Solar        | Delta   |" + color.END
        if abs(delta_az) <= 1.0:
            az_line = "|    Azimuth [deg] | {:+06.2f}   | {:+06.2f}      | ".format(lunar_az, solar_az)
            az_line += color.RED + "{:+06.3f}".format(delta_az) + color.END + "  |"
        else:        
            az_line = "|    Azimuth [deg] | {:+07.2f}   | {:+07.2f}      | {:+06.2f}  |".format(lunar_az, solar_az, delta_az)

        if abs(delta_el) <= 1.0:
            el_line = "|  Elevation [deg] | {:+06.2f}    | {:+06.2f}       | ".format(lunar_el, solar_el)
            el_line += color.RED + "{:+06.3f}".format(delta_el) + color.END + "  |"
        else:        
            el_line = "|  Elevation [deg] | {:+06.2f}    | {:+06.2f}       | {:+06.2f}  |".format(lunar_el, solar_el, delta_el)
        if (abs(delta_az) <= 1.0) and (abs(delta_el)<=1.0):
            print color.BOLD + az_line + color.END
            print color.BOLD + el_line + color.END
        else:
            print az_line
            print el_line
        
        print "|   Diameter [deg] | {:+0.4f}   | {:+0.4f}      | {:+0.4f} |".format(lunar_dia, solar_dia, delta_dia)
        print "|      Phase [%]   | {:06.3f}    | N/A          | N/A     |".format(m.moon_phase*100)
        print "|   Distance [km]  | {:08.2f} | {:08.2f} | N/A     |".format(lunar_r, solar_r)
        print "| Prop Delay [s]   | {:06.3f}    | {:06.3f}      | N/A     |".format(lunar_pd, solar_pd)
        print hor_hi
        print "       Separation [deg]: {:+3.3f}".format(separation)
        eclipse_status = "No Eclipse"
        if separation <= eclipse_condition: eclipse_status = color.RED + color.BOLD + "ECLIPSE" + color.END
        print "         Eclipse Status: {:s}".format(eclipse_status)
        
        overlap_area = Circle_Overlap(lunar_dia/2,solar_dia/2,separation)
        solar_area = math.pi * (solar_dia/2)**2
        overlap_percentage = overlap_area / solar_area
        #print "Area of Overlap [deg^2]: ", overlap_area
        #print "     Solar Area [deg^2]: ", solar_area
        print " Overlap Percentage [%]: {:3.6f}".format(overlap_area/solar_area*100)
        
        time.sleep(1)

    

    

sys.exit()
