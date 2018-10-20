"""
 *  PyDMXControl: A Python 3 module to control DMX via Python. Featuring fixture profiles and working with uDMX.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from enum import Enum
from typing import List, Dict, Tuple


class Colors(list, Enum):

    @staticmethod
    def mix(color1: List[int], color2: List[int], percent: float = 0.5) -> List[int]:
        if percent < 0 or percent > 1:
            percent = 0.5

        result = []
        for i in range(max(len(color1), len(color2))):
            val1 = color1[i] if i < len(color1) else 0
            val2 = color2[i] if i < len(color2) else 0
            val1 *= percent
            val2 *= 1 - percent
            res = val1 + val2
            res = min(res, 255)
            res = max(res, 0)
            result.append(int(res))

        return result

    @staticmethod
    def add(color1: List[int], color2: List[int], percent1: float = 1, percent2: float = 1) -> List[int]:
        if percent1 < 0 or percent1 > 1:
            percent1 = 1

        if percent2 < 0 or percent2 > 1:
            percent2 = 1

        result = []
        for i in range(max(len(color1), len(color2))):
            val1 = color1[i] if i < len(color1) else 0
            val2 = color2[i] if i < len(color2) else 0
            val1 *= percent1
            val2 *= percent2
            res = val1 + val2
            res = min(res, 255)
            res = max(res, 0)
            result.append(int(res))

        return result

    @staticmethod
    def to_dict(colors: List[int]) -> Dict[str, int]:
        """ Assumes RGBWA """
        keys = list('RGBWA')
        result = {}
        for i, color in enumerate(colors):
            if i < len(keys):
                result[keys[i]] = color
        return result

    @staticmethod
    def to_tuples(colors: List[int]) -> List[Tuple[str, int]]:
        """ Assumes RGBWA """
        return [(k, v) for k, v in Colors.to_dict(colors).items()]

    @staticmethod
    def to_hex(colors: List[int]) -> str:
        def clamp(x):
            return max(0, min(x, 255))

        result = "#"
        for color in colors:
            result += "{:02x}".format(clamp(color))
        return result

    @staticmethod
    def to_print(colors: List[int], separator: str = ", ") -> str:
        return separator.join([str(f) for f in colors])

    Black = [000, 000, 000, 000]
    White = [255, 255, 255, 255]
    Warm = [255, 127, 78, 000]
    Red = [255, 000, 000, 000]
    Amber = [255, 127, 000, 000]
    Yellow = [255, 255, 000, 000]
    Green = [000, 255, 000, 000]
    Cyan = [000, 255, 255, 000]
    Blue = [000, 000, 255, 000]
    Pink = [255, 105, 180, 000]
    UV = [75, 000, 130, 000]
    Magenta = [255, 000, 255, 000]
