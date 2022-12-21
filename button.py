from pygame_gui.elements.ui_button import UIButton


class CallbackButton(UIButton):
    def __init__(
		self,
        relative_rect,
        text: str = "",
        manager = None,
        container = None,
        object_id = None,
        anchors = None,
		callback= lambda event:...
    ):
        super().__init__(
            relative_rect,
            text,
            manager=manager,
            container=container,
            object_id=object_id,
            anchors=anchors,
        )
        self.callback = callback
