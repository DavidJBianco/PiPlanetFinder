#!/usr/bin/env python

from sense_hat import SenseHat
import time

SH_COLORS = {
                "red": (255, 0, 0),
                "orange": (255, 127, 0),
                "yellow": (255, 255, 0),
                "green": (0, 255, 0),
                "blue": (0, 0, 255),
                "indigo": (75, 0, 130),
                "violet": (159, 0, 255),
                "white": (255, 255, 255),
                "black": (0, 0, 0)
        }

W = SH_COLORS["white"]
B = SH_COLORS["black"]
G = SH_COLORS["green"]
R = SH_COLORS["red"]

SH_ARROWS = {
        "left": [B, B, B, B, B, B, B, B,
                 B, B, W, B, B, B, B, B,
                 B, W, B, B, B, B, B, B,
                 W, W, W, W, W, W, W, W,
                 B, W, B, B, B, B, B, B,
                 B, B, W, B, B, B, B, B,
                 B, B, B, B, B, B, B, B,
                 B, B, B, B, B, B, B, B],
        "right": [B, B, B, B, B, B, B, B,
                  B, B, B, B, B, W, B, B,
                  B, B, B, B, B, B, W, B,
                  W, W, W, W, W, W, W, W,
                  B, B, B, B, B, B, W, B,
                  B, B, B, B, B, W, B, B,
                  B, B, B, B, B, B, B, B,
                  B, B, B, B, B, B, B, B],
        "center": [B, B, B, W, W, B, B, B,
                   B, B, W, W, W, W, B, B,
                   B, W, B, W, W, B, W, B,
                   B, B, B, W, W, B, B, B,
                   B, B, B, W, W, B, B, B,
                   B, B, B, W, W, B, B, B,
                   B, B, B, W, W, B, B, B,
                   B, B, B, W, W, B, B, B],
        "down": [B, B, B, W, W, B, B, B,
                 B, B, B, W, W, B, B, B,
                 B, B, B, W, W, B, B, B,
                 B, B, B, W, W, B, B, B,
                 B, B, B, W, W, B, B, B,
                 B, W, B, W, W, B, W, B,
                 B, B, W, W, W, W, B, B,
                 B, B, B, W, W, B, B, B],
        "hold": [B, B, B, B, B, B, B, B,
                 B, B, B, B, B, B, B, B,
                 B, B, B, W, W, B, B, B,
                 B, B, W, B, B, W, B, B,
                 B, B, W, B, B, W, B, B,
                 B, B, B, W, W, B, B, B,
                 B, B, B, B, B, B, B, B,
                 B, B, B, B, B, B, B, B]
    }

SH_ONTARGET = [
        R, B, B, B, B, B, B, R,
        B, R, R, R, R, R, R, B,
        B, R, R, B, B, R, R, B,
        B, R, B, R, R, B, R, B,
        B, R, B, R, R, B, R, B,
        B, R, R, B, B, R, R, B,
        B, R, R, R, R, R, R, B,
        R, B, B, B, B, B, B, R,
    ]

SH_CHECKMARK = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, G,
        B, B, B, B, B, B, G, B,
        B, B, B, B, B, G, B, B,
        G, B, B, B, G, B, B, B,
        B, G, B, G, B, B, B, B,
        B, B, G, B, B, B, B, B,    
    ]

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
    print "Target: %d\tCurrent: %d\tDeviance: %d" % (target_altitude,
                                                     current_altitude,
                                                     deviance)

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
    i = 0
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
        
        if (i % 1) == 0:
            print current_azimuth
        i += 1

def find_altitude(sense, target_altitude=0, tolerance=5, min_successes=10):
    # Turn on the accelerometer
    sense.set_imu_config(compass_enabled=False,
                         gyro_enabled=True,
                         accel_enabled=True)

    i = 0
    target_readings = 0
    while target_readings < min_successes:
        current_altitude = get_altitude(sense, readings=10)

        sense.set_pixels(altitude_arrow(current_altitude, target_altitude=target_altitude, tolerance=tolerance))

        if abs(target_altitude - current_altitude) <= tolerance:
            target_readings += 1
        else:
            target_readings = 0

        if (i % 1) == 0:
            print current_altitude
        i += 1


##### MAIN #####

# Initialize the Sense Hat
sense = SenseHat()

# Clear the screen, set rotation and rig for low light running
sense.clear()
sense.set_rotation(90)
sense.low_light = True

try:
    while True:
        sense.show_message("Azimuth", text_colour=SH_COLORS["red"])
        find_azimuth(sense, target_azimuth=113, tolerance=5, min_successes=10)
        show_image(sense, image=SH_CHECKMARK)

        sense.show_message("Altitude", text_colour=SH_COLORS["red"])
        find_altitude(sense, target_altitude=33, tolerance=5, min_successes=10)
        show_image(sense, image=SH_CHECKMARK)

        # If we got here, we're ON TARGET!
        show_image(sense, image=SH_ONTARGET, flash=20, pause=3, clear=True)

        # By this point, we've found the object and the display is off.
        # If we click the joystick button, though, wake up and start over
        # again.
        button_pressed = False
        while not button_pressed:
            evt = sense.stick.wait_for_event()
            if evt.direction == "middle":
                button_pressed = True
            time.sleep(.5)
        
except (KeyboardInterrupt, Exception) as e:
    # On any kind of error, be sure to turn off the LEDs.
    sense.clear()
    print e
    

    

