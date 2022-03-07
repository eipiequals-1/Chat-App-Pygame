import pygame
import ui.font

class TextBox:
    def __init__(self, x, y, min_w, height, font_path, active_color=(0, 0, 0), passive_color=(220, 220, 220)):
        self.rect = pygame.Rect(x, y, min_w, height)
        self.default_w = min_w
        self.active_color = active_color
        self.passive_color = passive_color
        self.text = ""
        self.active = True
        self.font = ui.font.Font(font_path, round(height * 0.6))

    def draw(self, surface : pygame.Surface, bg_color : tuple, font_color=(0, 0, 0), border=2):
        # draw background
        pygame.draw.rect(surface, bg_color, self.rect)
        color = self.passive_color
        if self.active:
            color = self.active_color
        # draw border
        pygame.draw.rect(surface, color, self.rect, border)
        # draw text
        text_x = self.rect.left + border * 2
        text_y = self.rect.centery - self.font.font.get_height() / 2
        text = self.font.create_surf(self.text, font_color)
        surface.blit(text, (text_x, text_y))
        # draw cursor
        pygame.draw.line(surface, font_color, (text_x + text.get_width(), text_y), (text_x + text.get_width(), self.rect.bottom - border * 2), 2)
        # update dimenstions based off of text size
        new_w = max(self.default_w, text.get_width() + border * 5)
        self.rect.w = new_w

    def user_input(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
            else:
                self.text += event.unicode

    def backspace(self):
        self.text = self.text[:-1]

    def update(self, mouse):
        self.active = False
        if self.rect.collidepoint(mouse):
            self.active = True

    def get_text(self):
        return self.text

    def clear_text(self):
        self.text = ""