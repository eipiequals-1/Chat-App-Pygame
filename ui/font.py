import pygame

class Font:
    def __init__(self, path : str, size : int):
        self.font = pygame.font.Font(path, size)

    def render(self, surface : pygame.Surface, text : str, color : tuple, x : int, y : int):
        text_surf : pygame.Surface = self.create_surf(text, color)
        surface.blit(text_surf, (x, y))

    def render_centered(self, surface : pygame.Surface, text : str, color : tuple, centerx : int, y : int):
        text_surf : pygame.Surface = self.create_surf(text, color)
        surface.blit(text_surf, (centerx - text_surf.get_width() / 2, y))

    def create_surf(self, text : str, color : tuple) -> pygame.Surface:
        return self.font.render(text, 1, color)