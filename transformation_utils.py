import math
import sys
from shapes import Shape, Circle
import numpy as np



def apply_transformation(shape: Shape, transformation_matrix):
    for i, vertex in enumerate(shape.vertices):
        new_vertex = (np.matmul(transformation_matrix, [*vertex, 1])[:2]).astype(np.int32).tolist()
        shape.vertices[i] = new_vertex
        #TODO: bad design
        if isinstance(shape, Circle):
            shape.center = new_vertex



def translate(shape: Shape, tx, ty):
    translation_matrix = np.array(
        [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    apply_transformation(shape, translation_matrix)



def circle_scaling(circle: Circle, s):
    circle.radius *= s


def scale(shape: Shape, sx, sy):
    scaling_matrix = np.array(
        [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    apply_transformation(shape, scaling_matrix)

    if isinstance(shape, Circle):
        circle_scaling(shape, sx)


def rotate(shape: Shape, angle):
    angle = math.radians(angle)
    rotation_matrix = np.array(
        [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [              0,               0, 1]
        ])
    apply_transformation(shape, rotation_matrix)


def pivot_rotate(shape: Shape, angle, px, py):
    angle = math.radians(angle)
    shape_center = shape.get_center()
    tx, ty = shape_center[0] - px, shape_center[1] - py

    pivot_rotation_matrix = np.array(
        [
            [math.cos(angle), -math.sin(angle), -tx * math.cos(angle) + ty*math.sin(angle) + tx],
            [math.sin(angle), math.cos(angle), -tx * math.sin(angle) - ty*math.cos(angle) + ty],
            [              0,               0,                                              1]
        ])

    apply_transformation(shape, pivot_rotation_matrix)


def pivot_scale(shape: Shape, sx, sy, px, py):
    shape_center = shape.get_center()
    tx, ty = shape_center[0] - px, shape_center[1] - py

    pivot_scaling_matrix = np.array(
        [
            [sx, 0, -tx * sx + tx],
            [0, sy, -ty * sy + ty],
            [0, 0, 1]
        ])

    apply_transformation(shape, pivot_scaling_matrix)
    if isinstance(shape, Circle):
        circle_scaling(shape, sx)        


