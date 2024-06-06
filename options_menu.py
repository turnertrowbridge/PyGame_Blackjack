import pygame
from ui import draw_text, draw_button, draw_card, draw_hidden_card, draw_menu_card


class OptionsMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.BACKGROUND_COLOR_BUTTONS = [400, 300, 200, 100]
        self.GREEN_BUTTON = [275, 400, 200, 100]
        self.BLUE_BUTTON = [825, 400, 200, 100]
        self.PURPLE_BUTTON = [550, 400, 200, 100]
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.PURPLE = (255, 0, 255)
        self.show_background_color_menu = False

    def handle_events(self, event):
        if self.is_button_clicked(self.GREEN_BUTTON, event.pos):
            self.show_background_color_menu = False
            return self.GREEN
        elif self.is_button_clicked(self.BLUE_BUTTON, event.pos):
            self.show_background_color_menu = False
            return self.BLUE
        elif self.is_button_clicked(self.PURPLE_BUTTON, event.pos):
            self.show_background_color_menu = False
            return self.PURPLE
        return None

    def draw(self):
        # Draw background
        pygame.draw.rect(self.screen, (0, 0, 0), (180, 180, 960, 520))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (200, 200, 920, 480))
        draw_text(self.screen, self.font,
                  "Change Background Color", 440, 210)
        draw_button(self.screen, self.font, "Green", *self.GREEN_BUTTON, self.GREEN)
        draw_button(self.screen, self.font, "Blue", *self.BLUE_BUTTON, self.BLUE)
        draw_button(self.screen, self.font, "Purple", *self.PURPLE_BUTTON, self.PURPLE)

    def is_button_clicked(self, button, mouse_pos):
        return (button[0] <= mouse_pos[0] <= (button[0] + button[2]) and
                button[1] <= mouse_pos[1] <= (button[1] + button[3]))
