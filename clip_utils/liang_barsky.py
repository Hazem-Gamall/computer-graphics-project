from typing import Tuple


def liang_barsky(p1: Tuple, p2: Tuple, window_max: Tuple, window_min: Tuple) -> Tuple:      
    xmax, ymax = window_max
    xmin, ymin = window_min
    u1, u2 = 0, 1
    (x1,y1),(x2,y2) = p1, p2
    dx = x2-x1
    dy = y2-y1
    
    for i in range(4):
        if i == 0:
            p = -dx
            q = x1-xmin
        elif i == 1:
            p = dx
            q = xmax - x1
        elif i == 2:
            p = -dy
            q = y1 - ymin
        elif i ==3:
            p = dy
            q = ymax - y1
        
        if p == 0: 
            if q < 0:
                return None
        elif p < 0: 
            r = q/p
            u1 = max(u1, r)
        else: #p > 0
            r = q/p
            u2 = min(u2, r)
    
    if u1 > u2:
        return None
    p1 = ( round( x1 + (u1*dx) ), round( y1+ (u1*dy) ) )
    p2 = ( round( x1 + (u2*dx) ), round( y1+ (u2*dy) ) )

    return p1, p2

            