import pygame_gui


class HorizontalSlider(pygame_gui.elements.UIHorizontalSlider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_moving = False
        self.is_released = False

    def on_moved(self, event, movie_viewer):
        if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self:
                self.is_moving = True
                movie_viewer._is_rendering_frames = False
        else:
            if self.is_moving:
                self.is_released = True
            self.is_moving = False
            if self.is_released:
                movie_viewer._is_rendering_frames = True


class Button(pygame_gui.elements.UIButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_clicked(self, event, movie_viewer):
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self:
                movie_viewer._is_rendering_frames = not movie_viewer._is_rendering_frames
                print(movie_viewer._is_rendering_frames)
