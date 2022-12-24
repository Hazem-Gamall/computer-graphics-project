from shapes import Shape
import numpy as np


def translate(shape: Shape, tvalues):
    tx, ty = tvalues
    translation_matrix = np.array(
        [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    for i, vertex in enumerate(shape.vertices):
        print("new_vertex:", np.matmul(translation_matrix, [*vertex, 1]))
        new_vertex = (np.matmul(translation_matrix, [*vertex, 1])[:2]).astype(np.int32).tolist()
        shape.vertices[i] = new_vertex

    ...


def scale(shape: Shape, svalues):
    ...


def rotate(shape: Shape, angle):
    ...


def pivot_rotate(shape: Shape, angle, pivot):
    ...


def pivot_scale(shape: Shape, svalues, pivot):
    ...
