#!/usr/bin/env python

from sense_hat import SenseHat
import time


def show_image(sense, image, flash=False, frames=5, speed=0.1, clear=False):
    sense.set_pixels(image)
       
    if flash:
        i = 0
        
        while i < frames:
            time.sleep(speed)
            sense.clear()
            time.sleep(speed)
            sense.set_pixels(image)
            i += 1

    if clear:
        sense.clear()
        
def get_compass(sense, readings=1):
    i = 1
    while i <= readings:
        direction = sense.get_compass()
        i += 1

    direction = int(round(direction))

    return direction

def get_orientation(sense, readings=1):
    i = 1
    while i <= readings:
        orientation = sense.get_orientation()
        i += 1

    return orientation

def compass_arrow(current_bearing, target_bearing=0, tolerance=5):
    deviance = (target_bearing - current_bearing)
    print "Target: %d\tCurrent: %d\tDeviance: %d" % (target_bearing,
                                                     current_bearing,
                                                     deviance)
    if abs(deviance) <= tolerance :
        return SH_ARROWS["center"]
    elif (current_bearing > target_bearing) and (current_bearing <= 180 + target_bearing):
        print "LEFT"
        return SH_ARROWS["left"]
    else:
        print "RIGHT"
        return SH_ARROWS["right"]

def find_bearing(target_bearing=0):
    # Treat target_bearing of 360 as though it were 0 (which it is)
    target_bearing = target_bearing % 360
    i = 0
    
    while True:
        # For some reason, the compass likes to send both 0 and 360.
        # Even though they are the same, mathematically they are different.
        # So we basically don't allow 360, and make it always a 0 because
        # it fits better with our math.
        current_bearing = get_compass(sense, readings=10) % 360

        sense.set_pixels(compass_arrow(current_bearing, target_bearing=target_bearing, tolerance=5))
        
        if (i % 1) == 0:
            print current_bearing
        i += 1
    
    
sense = SenseHat()


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
                   B, B, B, W, W, B, B, B]
    }


sense.clear()
sense.set_rotation(90)
sense.low_light = True

try:
    find_bearing(360)
except (KeyboardInterrupt, Exception) as e:
    sense.clear()
    print e
    

    

