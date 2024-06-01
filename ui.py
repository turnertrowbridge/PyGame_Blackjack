import pygame

def draw_text(screen, font, text, x, y, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(screen, font, text, x, y, width, height, color=(255, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(screen, font, text, x + 10, y + 10)

def draw_card(screen, font, card, x, y, card_color=(255, 255, 255), text_color=(0, 0, 0)):
    pygame.draw.rect(screen, card_color, (x, y, 100, 150))
    draw_text(screen, font, str(card[0]), x + 10, y + 10, text_color)
    draw_text(screen, font, card[1], x + 10, y + 50, text_color)

