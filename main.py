import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1600, 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 50)
card_font = pygame.font.Font(None, 30)


HIT_BUTTON = [100, 800, 200, 100]
STAND_BUTTON = [500, 800, 200, 100]


# Function to draw text on the screen
def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))


# Function to draw text on a card
def draw_card_text(text, x, y):
    text_surface = card_font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))


# Function to draw a button on the screen
def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, RED, (x, y, width, height))
    draw_text(text, x + 10, y + 10)


# Function to draw a card on the screen
def draw_card(card, x, y):
    pygame.draw.rect(screen, RED, (x, y, 100, 150))
    draw_card_text(str(card[0]), x + 10, y + 10)
    draw_card_text(card[1], x + 10, y + 50)


# Function to create a deck of cards
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8',
             '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


# Function to deal a card
def deal_card(deck):
    return deck.pop()


# Function to calculate the total value of a hand
def calculate_total(hand):
    total = 0
    aces = 0
    for card in hand:
        if card[0] in ['Jack', 'Queen', 'King']:
            total += 10
        elif card[0] == 'Ace':
            total += 11
            aces += 1
        else:
            total += int(card[0])
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


# Game loop
running = True
deck = create_deck()
player_hand = [deal_card(deck), deal_card(deck)]
dealer_hand = [deal_card(deck), deal_card(deck)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if HIT_BUTTON[0] <= event.pos[0] <= (HIT_BUTTON[0] + HIT_BUTTON[2]) and HIT_BUTTON[1] <= event.pos[1] <= (HIT_BUTTON[1] + HIT_BUTTON[3]):
                player_hand.append(deal_card(deck))

            elif STAND_BUTTON[0] <= event.pos[0] <= (STAND_BUTTON[0] + STAND_BUTTON[2]) and STAND_BUTTON[1] <= event.pos[1] <= (STAND_BUTTON[1] + STAND_BUTTON[3]):
                while calculate_total(dealer_hand) < 17:
                    dealer_hand.append(deal_card(deck))

    # Draw everything
    screen.fill(GREEN)
    draw_text("Player's hand:", 100, 100)
    for i, card in enumerate(player_hand):
        draw_card(card, 100 + i * 110, 150)
    draw_text("Dealer's hand:", 100, 300)
    for i, card in enumerate(dealer_hand):
        draw_card(card, 100 + i * 110, 350)
    draw_button("Hit", HIT_BUTTON[0], HIT_BUTTON[1],
                HIT_BUTTON[2], HIT_BUTTON[3])
    draw_button(
        "Stand", STAND_BUTTON[0], STAND_BUTTON[1], STAND_BUTTON[2], STAND_BUTTON[3])

    # Check for wins
    player_total = calculate_total(player_hand)
    dealer_total = calculate_total(dealer_hand)
    if player_total > 21:
        draw_text("Player busts! Dealer wins!", 0, 0)
    elif dealer_total > 21:
        draw_text("Dealer busts! Player wins!", 0, 0)
    elif player_total == 21:
        draw_text("Player wins!", 100, 250)
    elif dealer_total == 21:
        draw_text("Dealer wins!", 100, 250)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
