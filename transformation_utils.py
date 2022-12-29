import math
import sys
from shapes import Shape, Circle, Ellipse
import numpy as np



def apply_transformation(point, transformation_matrix):
    new_point = (np.matmul(transformation_matrix, [*point, 1])[:2]).astype(np.int32).tolist()
    return new_point



def translate(point, **params):
    tx = params["tx"]
    ty = params["ty"]
    
    translation_matrix = np.array(
        [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

        

    return apply_transformation(point, translation_matrix)



def circle_scaling(circle: Circle, s):
    circle.radius *= s

def ellipse_scaling(ellipse:Ellipse, sx, sy):
    ellipse.xradius *= sx
    ellipse.yradius *= sy

def scale(point, **params):
    
    sx = params["sx"]
    sy = params["sy"]
    
    scaling_matrix = np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    return apply_transformation(point, scaling_matrix)


def rotate(point, **params):
    angle = params["angle"]
    angle = math.radians(angle)
    rotation_matrix = np.array(
        [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [              0,               0, 1]
        ])
    return apply_transformation(point, rotation_matrix)


def pivot_rotate(point, **params):
    center = params["center"]
    angle = params["angle"]
    px = params["px"]
    py = params["py"]

    angle = math.radians(angle)
    tx, ty = center[0] - px, center[1] - py

    pivot_rotation_matrix = np.array(
        [
            [math.cos(angle), -math.sin(angle), -tx * math.cos(angle) + ty*math.sin(angle) + tx],
            [math.sin(angle), math.cos(angle), -tx * math.sin(angle) - ty*math.cos(angle) + ty],
            [              0,               0,                                              1]
        ])

    return apply_transformation(point, pivot_rotation_matrix)


def pivot_scale(point, **params):
    center = params["center"]
    sx = params["sx"]
    sy = params["sy"]
    px = params["px"]
    py = params["py"]
    
    tx, ty = center[0] - px, center[1] - py

    pivot_scaling_matrix = np.array(
        [
            [sx, 0, -tx * sx + tx],
            [0, sy, -ty * sy + ty],
            [0, 0, 1]
        ])

    return apply_transformation(point, pivot_scaling_matrix)


def transform_shape(shape: Shape, transformation, **params):
    if isinstance(shape, (Circle, Ellipse)):
        shape.center = transformation(shape.center, **params)
        scaling_factors = [params.get("sx", 1), params.get("sy", 1)]

        if isinstance(shape, Circle):
            shape.radius *= scaling_factors[0]
        elif isinstance(shape, Ellipse):
            angle = params.get("angle", 0)
            shape.radius[0] *= scaling_factors[0]
            shape.radius[1] *= scaling_factors[1]
            shape.angle = angle
            
        
            

    for i, vertex in enumerate(shape.vertices):
        shape.vertices[i] = transformation(vertex, **params)
