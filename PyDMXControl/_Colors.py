"""
 *  PyDMXControl: A Python 3 module to control DMX using uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2018 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from enum import Enum
from typing import List, Dict, Tuple, Union

import itertools

class Colors(list, Enum):

    @staticmethod
    def clamp(val: Union[int, float]) -> int:
        """
        Clamp a color to ensure it fits in range [0..255]
        and convert it to an integer.

        Parameters
        ----------
        val: Value to clamp.

        Returns
        -------
        int
            Clamped value. [0..255]
        
        Examples
        --------

        >>> Colors.clamp(2323.52)
        255
        """
        return int(min(255, max(0, val)))

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
        for val1, val2 in itertools.zip_longest(color1, color2, fillvalue=0):
            val1 *= percent
            val2 *= 1 - percent
            res = Colors.clamp(val1 + val2)
            result.append(res)

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

        >>> Colors.add([0,128,0], [128,0,128], 1, 0.75)
        [96, 128, 96]
        """
        if percent1 < 0 or percent1 > 1:
            percent1 = 1

        if percent2 < 0 or percent2 > 1:
            percent2 = 1

        result = []
        for val1, val2 in itertools.zip_longest(color1, color2, fillvalue=0):
            val1 *= percent1
            val2 *= percent2
            res = Colors.clamp(val1 + val2)
            result.append(res)

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

        >>> Colors.to_dict([1,2,3,4,5]) 
        {'R': 1, 'G': 2, 'B': 3, 'W': 4, 'A': 5}
        """
        return dict(zip('RGBWA', colors))

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

        >>> Colors.to_tuples([1,2,3,4,5]) 
        [('R', 1), ('G', 2), ('B', 3), ('W', 4), ('A', 5)]
        """
        return list(zip('RGBWA', colors))

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

        >>> Colors.to_hex([95, 93, 12])
        '#5f5d0c'
        """

        result = "#"
        for color in colors:
            result += "{:02x}".format(Colors.clamp(color))
        return result

    @staticmethod
    def to_print(colors: List[int], separator: str = ", ") -> str:
        """Convert a color from list form to a printable string.

        Parameters
        ----------
        colors: Color to convert to printable form.
        separator: Separator to use.

        Returns
        -------
        str
            Color as a printable string.

        Examples
        --------

        >>> Colors.to_print([95, 93, 12, 18, 128]) 
        '95, 93, 12, 18, 128'
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
