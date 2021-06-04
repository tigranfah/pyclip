from clip import Position


class GuiComponent:

    def __init__(self, pos, width, height):
        self.position = pos
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.bg_image = None
        self.subcomponents = []


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

class Slider(GuiComponent):

    def __init__(self, pos, width, height, range):
        GuiComponent.__init__(pos, width, height)

        self._slider = Button(Position(pos.x, pos.y), width=20, height)
        # self._time_line = GuiComponent()
        self._current_index = 0

    def slide(self, x_pos):
        if x_pos <= self.position.x or x_pos >= self.position.x + self.width: return
        self._slider.position.x = x_pos
        # self._current_index = self._current_index + move_by

    @property
    def current_index(self):
        return self._current_index



class ControlBar(GuiComponent):

    def __init__(self, pos, width, height):
        GuiComponent.__init__(pos, width, height)

        self._stop_resume_button = StopResumeButton()