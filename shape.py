
class Shape():
    def __init__(self, num_of_vertices) -> None:
        self.vertices = []
        self.vertex_counter = 0
        self.max_vertices = num_of_vertices

    def set_vertex(self, vertex):
        print(self.vertex_counter)

        self.vertices.append(vertex)
        self.vertex_counter+=1
        print(self.vertices)
        if self.vertex_counter >= self.max_vertices:
            return True
        return False
