import numpy as np
from enum import Enum


class DistUnit(Enum):
    METERS = 1
    CENTIMETERS = 100
    FEET = 3.2808399
    INCHES = 39.3700787


class AngleUnit(Enum):
    RADIANS = 1
    DEGREES = 57.29577951308232
