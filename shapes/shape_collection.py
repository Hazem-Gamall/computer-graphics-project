from typing import Union, Iterable

from shapes import Shape

class ShapeCollection:
    def __init__(self, collection = []) -> None:
        self.collection = collection
    
    def add(self, shapes: Union[Shape, Iterable]):
        if isinstance(shapes, Iterable):
            self.collection += shapes
            return

        self.collection.append(shapes)
    

    
