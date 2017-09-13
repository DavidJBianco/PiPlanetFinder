#!/usr/bin/env python

import traceback
from sense_hat import SenseHat
import time
import sys
import gps
import ephem
import os

from util.colors import *
from util.bitmaps import *

targets = [
            ephem.Mercury(),
            ephem.Venus(),
            ephem.Mars(),
            ephem.Jupiter(),
            ephem.Saturn(),
            ephem.Uranus(),
            ephem.Neptune(),
            ephem.Pluto(),
            ephem.Sun(),
            ephem.Moon()
    ]


def wait_for_command(sense, min_gforce=3):
    '''
    Wait for one of two things to happen.  Either the joytstick button
    was clicked (in which case return True), or the pi was shaken (not stirred).
    If this is the case, then shut down the whole computer gracefully.

    min_gforce controls how hard you have to shake the device in order to
    trigger the shutdown.  The default is three, which is a pretty good
    shake and unlikely to be triggered by random arm movements while
    simply holding or carrying the device.
    '''
    got_command = False

    # empty the event queue in case there are stray joystick pushes
    # that would cause us to immediately proceed
    sense.stick.get_events()
    while not got_command:
        evts = sense.stick.get_events()
        for evt in evts:
            if evt.direction == "middle":
                got_command = True
                return True

        x, y, z = sense.get_accelerometer_raw().values()

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if (x > min_gforce) or (y > min_gforce) or (z > min_gforce):
            # We're all shook up!
            sense.show_message("Shutdown", text_colour=R)
            #os.system("/sbin/shutdown -h now")
            sys.exit(0)
            
        time.sleep(.5)

    return evt    


def select_target(sense, targets):
    i = 0
    while True:
        sense.show_message(targets[i].name, text_colour=R)
        evt = None
        while not evt:
            evt = sense.stick.wait_for_event()
            print evt
            if evt.action == 'pressed':
                if evt.direction == "middle":
                    return targets[i]
                elif evt.direction == "left":
                    i = (i + 1) % len(targets)
                elif evt.direction == "right":
                    i = (i - 1) % len(targets)
            else:
                evt = None

def format_date(d):
    '''
    Convert a timestamp string provided by the GPS into a format that the
    ephem module can understand.  The return result is also a string, just
    in a different format.
    '''
    return time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ"))

def get_gps_info():
    # Turn on the GPS
    session = gps.gps(mode=gps.WATCH_ENABLE)

    # Loop until we get a mode 3 message (3D lock acquired)
    gps_fix = False
    while not gps_fix:
        report = session.next()
        print report
        # GPS has many message types, but TPV is the only one we care about.
        # Skip all the others.
        if report["class"] == "TPV":
            if report["mode"] in [2,3]:
                # We got a 3D GPS fix
                gps_fix = True
                latitude = report["lat"]
                longitude = report["lon"]
                utc_time = report["time"]

        # Sleep a bit, just to avoid going into a tight loop
        time.sleep(0.1)

    # Turn off GPS to conserve battery
    session = gps.gps(mode=gps.WATCH_DISABLE)
    
    return (latitude, longitude, utc_time)

def show_image(sense, image, flash=False, frames=5, speed=0.1,
               pause=3, clear=False):
    sense.set_pixels(image)
       
    if flash:
        i = 0
        
        while i < frames:
            time.sleep(speed)
            sense.clear()
            time.sleep(speed)
            sense.set_pixels(image)
            i += 1

    time.sleep(pause)

    if clear:
        sense.clear()
        
def get_compass(sense, readings=1):
    i = 1
    while i <= readings:
        direction = sense.get_compass()
        i += 1

    direction = int(round(direction))

    return direction

def get_altitude(sense, readings=1):
    i = 1
    while i <= readings:
        pitch = sense.get_orientation()["pitch"]
        i += 1

    return pitch

def azimuth_arrow(current_azimuth, target_azimuth=0, tolerance=5):
    deviance = (target_azimuth - current_azimuth)

    if abs(deviance) <= tolerance :
        return SH_ARROWS["center"]
    elif (current_azimuth > target_azimuth) and (current_azimuth <= 180 + target_azimuth):
        return SH_ARROWS["left"]
    else:
        return SH_ARROWS["right"]

def altitude_arrow(current_altitude, target_altitude=0, tolerance=5):
    deviance = (target_altitude - current_altitude)

    if abs(deviance) <= tolerance:
        return SH_ARROWS["hold"]
    else:
        return SH_ARROWS["center"] # also an UP arrow

def find_azimuth(sense, target_azimuth=0, tolerance=5, min_successes=10):
    # Turn on the magnetometer
    sense.set_imu_config(compass_enabled=True,
                         gyro_enabled=False,
                         accel_enabled=False)
    
    # Treat target_azimuth of 360 as though it were 0 (which it is)
    target_azimuth = target_azimuth % 360

    target_readings = 0
    while target_readings < min_successes:
        # For some reason, the compass likes to send both 0 and 360.
        # Even though they are the same, mathematically they are different.
        # So we basically don't allow 360, and make it always a 0 because
        # it fits better with our math.
        current_azimuth = get_compass(sense, readings=10) % 360

        sense.set_pixels(azimuth_arrow(current_azimuth, target_azimuth=target_azimuth, tolerance=tolerance))

        if abs(target_azimuth - current_azimuth) <= tolerance:
            target_readings += 1
        else:
            target_readings = 0
        

def find_altitude(sense, target_altitude=0, tolerance=5, min_successes=10):
    # Turn on the accelerometer
    sense.set_imu_config(compass_enabled=False,
                         gyro_enabled=True,
                         accel_enabled=True)

    target_readings = 0
    while target_readings < min_successes:
        current_altitude = get_altitude(sense, readings=10)

        sense.set_pixels(altitude_arrow(current_altitude, target_altitude=target_altitude, tolerance=tolerance))

        if abs(target_altitude - current_altitude) <= tolerance:
            target_readings += 1
        else:
            target_readings = 0


##### MAIN #####

# Initialize the Sense Hat
sense = SenseHat()

# Clear the screen, set rotation and rig for low light running
sense.clear()
sense.set_rotation(90)
sense.low_light = True

try:
    while True:
        # For accurate ephemera, we need to get our current latitude, longitude,
        # altitude and time from the GPS
        sense.show_message("GPS", text_colour=R)

        (latitude, longitude, utc_time) = get_gps_info()
        print "Lat/Lon: %s, %s" % (latitude, longitude)
        print "Time: %s" % utc_time

        show_image(sense, image=SH_CHECKMARK, clear=True)

        # Determine the celestial coordinates of our test object, the Sun

        obj = select_target(sense, targets)
        print "Target: %s" % obj.name
        show_image(sense, image=SH_CHECKMARK, clear=True)
       
        observer = ephem.Observer()
        observer.lon = longitude
        observer.lat = latitude
        observer.date = format_date(utc_time)

        obj.compute(observer)

        # Ephem returns the azimuth and altitude as colon-separated strings
        # (e.g. "70:01:03.5" for "70 degrees and change).  We only need the first
        # value, since our pointing device's accuracy is kinda rough anyway.
        # So split those off and convert them to integers
        target_azimuth = int(str(obj.az).split(":")[0])
        target_altitude = int(str(obj.alt).split(":")[0])

        print "Target Azimuth: %s" % target_azimuth
        print "Target Altitude: %s" % target_altitude

        sense.show_message("Azimuth: %d" % target_azimuth, text_colour=SH_COLORS["red"])
        find_azimuth(sense, target_azimuth=target_azimuth, tolerance=5, min_successes=10)
        show_image(sense, image=SH_CHECKMARK)

        sense.show_message("Altitude: %d" % target_altitude, text_colour=SH_COLORS["red"])
        find_altitude(sense, target_altitude=target_altitude, tolerance=5, min_successes=10)
        show_image(sense, image=SH_CHECKMARK)

        # If we got here, we're ON TARGET!
        show_image(sense, image=SH_ONTARGET, flash=20, pause=3, clear=True)

        # By this point, we've found the object and the display is off.
        # If we click the joystick button, though, wake up and start over
        # again.  Or maybe we want to shake the device and shutdown the system.
        wait_for_command(sense)
        
except (KeyboardInterrupt, Exception) as e:
    # On any kind of error, be sure to turn off the LEDs and the GPS.
    sense.clear()
    gps.gps(mode=gps.WATCH_DISABLE)

    # Print a traceback so we can figure out what went wrong, unless it was
    # keyboard interrupt (CTRL-C, presumably from the user)
    if not type(e) == KeyboardInterrupt:
        print traceback.format_exc()


    

    

