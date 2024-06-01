import pygame


def draw_text(screen, font, text, x, y, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_button(screen, font, text, x, y, width, height, color=(255, 0, 0)):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(screen, font, text, x + 10, y + 10)


def draw_card(screen, font, card, x, y, card_color=(255, 255, 255), text_color=(0, 0, 0)):
    pygame.draw.rect(screen, card_color, (x, y, 100, 150))
    # draw_text(screen, font, card[1], x + 10, y + 50, text_color)  # Suit name
    draw_text(screen, font, card[2], x + 10, y + 10, text_color)  # top left

    # draw bottom right upside down
    text_surface = font.render(card[2], True, text_color)
    flipped_text_surface = pygame.transform.flip(text_surface, False, True)
    screen.blit(flipped_text_surface, (x + 80, y + 130))  # bottom left

    # Add sprite
    card_sprite = pygame.image.load(f"./images/{card[1].lower()}.png")
    card_sprite = pygame.transform.scale(card_sprite, (50, 50))
    screen.blit(card_sprite, (x + 25, y + 50))
