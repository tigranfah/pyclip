import pygame
import numpy as np


class MouseEventType:

    def __init__(self):
        self._event_dict = {}
        self.set_default()

    def set_default(self):
        self._event_dict = {
            "LEFT" : False,
            "RIGHT" : False,
            "WHEEL" : False,
            "UP_SCROLL" : False,
            "DOWN_SCROLL" : False
        }

    def get_event(self, name):
        return self._event_dict[name]

    def set_event(self, index):
        ev_name = {
            1 : "LEFT",
            2 : "WHEEL",
            3 : "RIGHT",
            4 : "UP_SCROLL",
            5 : "DOWN_SCROLL"
        }[index]
        self._event_dict[ev_name] = True

    def __str__(self):
        return str(self._event_dict)


class MouseEvent:

    def __init__(self):
        self.is_clicked = False
        self.is_pressed = False

        self.event_type = MouseEventType()

        self.position = None

    def __no_event(self):
        self.is_clicked = False
        self.is_pressed = False

        self.event_type.set_default()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # sometimes event.button was getting values 6 and 7, which are not shown in docs
            if event.button > 5: return
            self.is_clicked = True
            self.event_type.set_event(event.button)
        elif any(pygame.mouse.get_pressed()):
            self.is_pressed = True
            ind = np.argwhere(np.array(pygame.mouse.get_pressed()) == True)[0][0] + 1
            self.event_type.set_event(ind)
        else:
            self.__no_event()

        self.position = pygame.mouse.get_pos()