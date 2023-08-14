import numpy as np
from Enum import enum


class DistUnit(enum):
    METERS = 1
    CENTIMETERS = 100
    FEET = 3.2808399
    INCHES = 39.3700787


class AngleUnit(enum):
    RADIANS = 1
    DEGREES = 57.29577951308232
