from abc import ABCMeta, abstractmethod

class BaseState(metaclass=ABCMeta):
    def __init__(self, game) -> None:
        self.game = game
        self.substate = None
        self.game.reset_state_panel()

    def update(self) -> None:
        ...

    def draw(self) -> None:
        ...

    def on_click(self, event) -> None:
        ...

    def change_substate(self, new_substate):
        self.substate = new_substate
        
    @abstractmethod
    def on_exit(self):
        ...




