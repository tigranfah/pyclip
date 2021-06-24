import pygame
import cv2


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

    def clear(self):
        self._display.fill((0, 0, 0))

    def render_frame(self, frame, position, scale, rotation_angle):

        surface = Converter.frame_to_surface(frame).convert_alpha()
        # surface = pygame.transform.scale(surface, (scale.w, scale.h))
        surface = pygame.transform.rotate(surface, rotation_angle)
        self._display.blit(surface, (position.x, position.y))

    def render_gui_component(self, comp):
        if comp.color:
            pygame.draw.rect(self._display, comp.color, (comp.position.x, comp.position.y, comp.width, comp.height))

        for sub_comp in comp.subcomponents:
            self.render_gui_component(sub_comp)