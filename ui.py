import pygame


def draw_text(screen, font, text, x, y, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_button(screen, font, text, x, y, width, height, color=(255, 0, 0)):
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height),
                     2)  # Draw black border
    pygame.draw.rect(screen, color, (x + 2, y + 2, width - 4,
                     height - 4))  # Draw button background
    draw_text(screen, font, text, x + 10, y + 10)


def draw_card(screen, font, card, x, y, card_color=(255, 255, 255), text_color=(0, 0, 0)):
    width, height = 100, 150
    pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4),
                     2)  # Draw black border
    pygame.draw.rect(screen, card_color, (x, y, width,
                     height))  # Draw button background
    draw_text(screen, font, card[2], x + 10, y + 10, text_color)  # top left

    # draw bottom right upside down
    text_surface = font.render(card[2], True, text_color)
    flipped_text_surface = pygame.transform.flip(text_surface, False, True)
    screen.blit(flipped_text_surface, (x + 80, y + 130))  # bottom left

    # Add sprite
    card_sprite = pygame.image.load(f"./images/{card[1].lower()}.png")
    card_sprite = pygame.transform.scale(card_sprite, (50, 50))
    screen.blit(card_sprite, (x + 25, y + 50))


def draw_menu_card(screen, font, card, x, y, card_color=(255, 255, 255), text_color=(0, 0, 0)):
    modifier = 1.5
    width, height = 100, 150
    width *= modifier
    height *= modifier
    pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4),
                     2)  # Draw black border
    pygame.draw.rect(screen, card_color, (x, y, width,
                     height))  # Draw button background
    draw_text(screen, font, card[2], x + 10, y + 10, text_color)  # top left

    # draw bottom right upside down
    text_surface = font.render(card[2], True, text_color)
    flipped_text_surface = pygame.transform.flip(text_surface, False, True)
    screen.blit(flipped_text_surface, (x + (80 * modifier), y + (130 * modifier)))
    # Add sprite
    card_sprite=pygame.image.load(f"./images/{card[1].lower()}.png")
    card_sprite=pygame.transform.scale(
        card_sprite, (50 * modifier, 50 * modifier))
    screen.blit(card_sprite, (x + (25 * modifier), y + (50 * modifier)))


def draw_hidden_card(screen, font, x, y):
    width, height=100, 150
    pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, width +
                     4, height + 4), 2)  # Draw black border
    card_back=pygame.image.load("./images/card_back.png")
    card_back=pygame.transform.scale(card_back, (width, height))
    screen.blit(card_back, (x, y))
