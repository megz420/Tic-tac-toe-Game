import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        # Initialize the button with its position, size, text, and colors
        self.rect = pg.Rect(x, y, width, height)  # Define the button's rectangular area
        self.text = text  # Text to display on the button
        self.color = color  # Button's default color
        self.hover_color = hover_color  # Button's color when hovered over

    def draw(self, screen):
        # Draw the button on the screen
        font = pg.font.SysFont(None, 48)  # Use a system font for the button text
        white = (255, 255, 255)  # Define the color white for text

        # Check if the mouse is currently over the button
        mouse_pos = pg.mouse.get_pos()  # Get the current mouse position
        if self.rect.collidepoint(mouse_pos):  # Check if the mouse is within the button's area
            pg.draw.rect(screen, self.hover_color, self.rect)  # Draw the button with hover color
        else:
            pg.draw.rect(screen, self.color, self.rect)  # Draw the button with its default color

        # Render the text on the button
        text_surface = font.render(self.text, True, white)  # Render the text as a surface
        text_rect = text_surface.get_rect(center=self.rect.center)  # Center the text on the button
        screen.blit(text_surface, text_rect)  # Draw the text on the screen

    def is_clicked(self, event, pg_mousebuttondown):
        # Check if the button is clicked
        if event.type == pg_mousebuttondown:  # Check if the event is a mouse button press
            if self.rect.collidepoint(event.pos):  # Check if the click happened within the button's area
                return True  # Button was clicked
        return False  # Button was not clicked
