import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        font = pg.font.SysFont(None, 48)
        white = (255 ,255 ,255)
        # Check if the mouse is over the button
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(screen, self.hover_color, self.rect)
        else:
            pg.draw.rect(screen, self.color, self.rect)

        # Render the text on the button
        text_surface = font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event, pg_mousebuttondown):
        if event.type == pg_mousebuttondown:
            if self.rect.collidepoint(event.pos):
                return True
        return False