from clip import Position


class GuiComponent:

    def __init__(self, pos, width, height):
        self.position = pos
        self.width = width
        self.height = height


class Button(GuiComponent):

    def __init__(self, pos, width, height):
        GuiComponent.__init__(self, pos, width, height)
        self._click_callback = None

    def on_click_callback(self, click_callback):
        self._click_callback = click_callback

    def is_clicked(self, x, y):
        if x >= self.position.x and y >= self.position.y:
            if x <= self.position.x + self.width and y <= self.position.y + self.height:
                return True
        return False

    def on_click(self, *args, **kwargs):
        self._click_callback(*args, **kwargs)


class StopResumeButton(Button):

    def __init__(self, pos, width, height):
        Button.__init__(self, pos, width, height)

        self.is_on = False
        self.on_click_callback(self.__on_click_callback)

    def __on_click_callback(self):
        if self.is_on:
            self.is_on = False
        else:
            self.is_on = True


class TimeLine(GuiComponent):

    def __init__(self, pos, width, height):
        GuiComponent.__init__(pos, width, height)