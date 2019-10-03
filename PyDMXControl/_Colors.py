"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from enum import Enum
from typing import List, Dict, Tuple


class Colors(list, Enum):

    @staticmethod
    def mix(color1: List[int], color2: List[int], percent: float = 0.5) -> List[int]:
        """Mix two colors, with an optional percentage.

        Mixes `percent` of color1 with 1-`percent` of color2.

        Parameters
        ----------
        color1: The first color.
        color2: The second color.
        percent: Ratio in which two colors are to be mixed (0..1).

        Returns
        -------
        List[int]
            New color after mixing.
        
        Examples
        --------

        >>> Colors.mix([0,128,0], [128,0,128], 0.5)    
        [64, 64, 64]
        """
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
        """Add two colors.

        Adds `percent1` of color1 with `percent2` of color2.

        Parameters
        ----------
        color1: The first color.
        color2: The second color.
        percent1: Percentage of brightness of color 1 (0..1).
        percent2: Percentage of brightness of color 2 (0..1).

        Returns
        -------
        List[int]
            New color after mixing.
        
        Examples
        --------

        >>> Colors.mix([0,128,0], [128,0,128], 0.5)  
        [64, 64, 64]
        """
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
        """Convert a color from list form to a dict.
        
        Assumes RGBWA.
        
        Parameters
        ----------
        colors: Color to convert to a dictionary.

        Returns
        -------
        Dict[str, int]
            Color as a dictionary.

        Examples
        --------

        >>> PyDMXControl.Colors.to_dict([1,2,3,4,5]) 
        {'R': 1, 'G': 2, 'B': 3, 'W': 4, 'A': 5}
        """
        keys = list('RGBWA')
        result = {}
        for i, color in enumerate(colors):
            if i < len(keys):
                result[keys[i]] = color
        return result

    @staticmethod
    def to_tuples(colors: List[int]) -> List[Tuple[str, int]]:
        """Convert a color from a list to a list of tuples.
        
        Assumes RGBWA.
        
        Parameters
        ----------
        colors: Color to convert to tuples.

        Returns
        -------
        List[Tuple[str, int]]
            Color as a list of tuples.

        Examples
        --------

        >>> PyDMXControl.Colors.to_tuples([1,2,3,4,5]) 
        [('R', 1), ('G', 2), ('B', 3), ('W', 4), ('A', 5)]
        """
        return [(k, v) for k, v in Colors.to_dict(colors).items()]

    @staticmethod
    def to_hex(colors: List[int]) -> str:
        """Convert a color from list to hex form.

        Parameters
        ----------
        colors: Color to convert to tuples.

        Returns
        -------
        str
            Color as a hex string.

        Examples
        --------

        >>> PyDMXControl.Colors.to_hex([95, 93, 12, 18, 128])
        '#5f5d0c1280'
        """

        def clamp(x):
            return max(0, min(x, 255))

        result = "#"
        for color in colors:
            result += "{:02x}".format(clamp(color))
        return result

    @staticmethod
    def to_print(colors: List[int], separator: str = ", ") -> str:
        """Convert a color from list form to a printable string.

        Parameters
        ----------
        colors: Color to convert to printable form.
        separator: Separator to use,

        Returns
        -------
        str
            Color as a hex string.

        Examples
        --------

        >>> PyDMXControl.Colors.to_hex([95, 93, 12, 18, 128])
        '#5f5d0c1280'
        """

        return separator.join([str(f) for f in colors])

    Black = [000, 000, 000, 000]
    White = [255, 255, 255, 255]
    Warm = [255, 170, 85, 85]
    Red = [255, 000, 000, 000]
    Amber = [255, 127, 000, 000]
    Yellow = [255, 255, 000, 000]
    Green = [000, 255, 000, 000]
    Cyan = [000, 255, 255, 000]
    Blue = [000, 000, 255, 000]
    Pink = [255, 105, 180, 000]
    UV = [75, 000, 130, 000]
    Magenta = [255, 000, 255, 000]
