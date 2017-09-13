#!/usr/bin/env python

from colors import *

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
