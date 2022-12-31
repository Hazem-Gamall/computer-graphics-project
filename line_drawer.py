from drawing_utils import bresenham, dda

line_drawer = bresenham

def change_drawer(drawer):
    global line_drawer
    if drawer == "DDA":
        print("new drawer dda")
        line_drawer = dda
    elif drawer == "Bresenham":
        print("new drawer bresenham")
        line_drawer = bresenham

def get_line_drawer():
    return line_drawer