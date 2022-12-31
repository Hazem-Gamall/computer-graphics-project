from clip_utils.cohen_sutherland import cohen_sutherland
from clip_utils.liang_barsky import liang_barsky

clipper_algorithm = liang_barsky

def change_clipper_algorithm(drawer):
    global clipper_algorithm
    if drawer == "Liang Barsky":
        print("new drawer dda")
        clipper_algorithm = liang_barsky
    elif drawer == "Cohen Sutherland":
        print("new drawer bresenham")
        clipper_algorithm = cohen_sutherland

def get_clipper_algorithm():
    return clipper_algorithm