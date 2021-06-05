import pygame_gui

from clip import Position


class GuiComponent:

    def __init__(self, pos, width, height):
        self.position = pos
        self.width = width
        self.height = height
        self.color = None
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

class SlideButton(Button):

    def __init__(self, pos, width, height):
        Button.__init__(self, pos, width, height)

        self.is_pressed = False
        self.on_click_callback(self.__on_slide_callback)

    def is_clicked(self, x, y):
        if self.is_pressed:
            return True
        self.is_pressed = Button.is_clicked(self, x, y)
        return self.is_pressed

    def __on_slide_callback(self, x_pos):
        self.position.x = x_pos

class Slider(GuiComponent):

    def __init__(self, pos, width, height, range):
        GuiComponent.__init__(self, pos, width, height)

        self.slider_button = SlideButton(Position(pos.x, pos.y), 20, height)
        self.slider_button.color = (255, 255, 255)
        self.time_line = GuiComponent(Position(pos.x, pos.y), width, height)
        self.time_line.color = (150, 150, 150)
        self._current_index = 0
        self.subcomponents.append(self.time_line)
        self.subcomponents.append(self.slider_button)

    def slide(self, x_pos):
        if x_pos <= self.position.x or x_pos >= self.position.x + self.width: return
        self.slider_button.on_click(x_pos)

    @property
    def current_index(self):
        return self._current_index


class ControlBar:

    def __init__(self):

        pass
        # GuiComponent.__init__(self, pos, width, height)

        # # self._stop_resume_button = StopResumeButton()
        # self.slider = Slider(pos, width, height * 0.5, (0, 1000))
        # self.subcomponents.append(self.slider)