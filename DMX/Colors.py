from enum import Enum
from typing import List


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
            result.append(res)

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
            result.append(res)

        return result

    Black   = [000, 000, 000]
    White   = [255, 255, 255]
    Red     = [255, 000, 000]
    Amber   = [255, 127, 000]
    Yellow  = [255, 255, 000]
    Green   = [000, 255, 000]
    Cyan    = [000, 255, 255]
    Blue    = [000, 000, 255]
    Pink    = [255, 105, 180]
    UV      = [ 75, 000, 130]
    Magenta = [255, 000, 255]
