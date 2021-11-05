import pygame
import cv2

import copy
import enum


class Converter:

    @staticmethod
    def surface_to_frame(surface):
        frame = pygame.surfarray.pixels3d(pygame.transform.rotate(pygame.transform.flip(surface, True, False), 90))
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return bgr_frame

    @staticmethod
    def frame_to_surface(frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        numpy_frame_surf = pygame.surfarray.make_surface(rgb_frame)
        frame_surf = pygame.transform.rotate(pygame.transform.flip(numpy_frame_surf, False, True), -90)
        return frame_surf


class Renderer:

    def __init__(self, display):

        self._display = display

    def clear(self, color):
        self._display.fill(color)

    def render_frame(self, w, h, frame, trans):

        resized_frame = cv2.resize(frame, (int(w * trans.scale.w), int(h * trans.scale.h)), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

        surface = Converter.frame_to_surface(resized_frame).convert_alpha()
        surface = pygame.transform.rotate(surface, trans.rot.angle)

        self._display.blit(surface, (w * trans.pos.x, h * trans.pos.y))

    def render_gui_component(self, comp):
        if comp.color:
            pygame.draw.rect(self._display, comp.color, (comp.position.x, comp.position.y, comp.width, comp.height))

        for sub_comp in comp.subcomponents:
            self.render_gui_component(sub_comp)
