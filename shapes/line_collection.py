import math
from typing import Union, Iterable

from pygame import Rect

from shapes import ICollides, Line

class LineCollection(ICollides):
    def __init__(self, collection = []) -> None:
        self.collection: Iterable[Line] = []
        self.vertices = []
        self.add(collection)
    
    def add(self, lines: Union[Line, Iterable]):
        if isinstance(lines, Iterable):
            self.collection += lines
        else:
            self.collection.append(lines)
        for line in self.collection:
            self.vertices.append(line.vertices)

    def get_bounding_rect(self) -> Rect:
        min_p = [math.inf]*2
        max_p = [-math.inf]*2

        for line in self.collection:
            (x1,y1), (x2,y2) = line.vertices
            min_p[0] = min(x1,x2, min_p[0])
            min_p[1] = min(y1,y2, min_p[1])
            max_p[0] = max(x1,x2, max_p[0])
            max_p[1] = max(y1,y2, max_p[1])

        left, top = min_p[0], min_p[1]
        width, height = max_p[0] - left, max_p[1] - top
        # print(f"max_p:{max_p}\nmin_p:{min_p}\nleft:{left}, top:{top}, width:{width}, height:{height}")
        return Rect(left, top, width, height)
    
    def get_center(self) -> Iterable:
        return super().get_center()