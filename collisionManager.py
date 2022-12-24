from pygame import Rect

def check_rect_point_collision(rect: Rect, point):
        if point[0] in range(rect.left, rect.right) and point[1] in range(rect.top, rect.bottom):
            print(rect)
            return True
        else:
            return False