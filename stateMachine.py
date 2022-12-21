from singleton import Singleton
class StateMachine(metaclass=Singleton):
        __current_state = None

        def initialize(self, game):
            self.game = game

        def change_state(self, new_state):
            self.__current_state = new_state

        @property
        def state(self):
            return self.__current_state

        def update(self):
            self.__current_state.update()

        def draw(self):
            self.__current_state.draw()