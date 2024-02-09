"""
Holds the types used in musicxml.py
"""

from enum import Enum


class Syllabic(Enum):
    """
    Syllabic values
    """

    SINGLE = "single"
    BEGIN = "begin"
    MIDDLE = "middle"
    END = "end"


class BeamType(Enum):
    """
    Beam types
    """

    BEGIN = "begin"
    CONTINUE = "continue"
    END = "end"


class TieType(Enum):
    """
    Tie type
    """

    START = "start"
    STOP = "stop"


class StemType(Enum):
    """
    The direction the note stem is in
    """

    UP = "up"
    DOWN = "down"
    NONE = "none"
    DOUBLE = "double"


class ClefSign(Enum):
    """
    The types of clefs and values
    """

    TREBLE = "G"
    BASS = "F"
    ALTO = "C"
    PERCUSSION = "percussion"


class BarLocation(Enum):
    """
    The location of the barline on a measure
    """

    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"


class BarStyle(Enum):
    """
    The weighting of the barline
    """

    LIGHT_LIGHT = "light-light"
    LIGHT_HEAVY = "light-heavy"
    HEAVY_LIGHT = "heavy-light"
    HEAVY_HEAVY = "heavy-heavy"
    DOTTED = "dotted"
    DOUBLE = "double"
    FINAL = "final"
    REGULAR = "regular"
    SHORT = "short"
    TICK = "tick"
