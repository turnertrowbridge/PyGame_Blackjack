import pygame
from ui import draw_text, draw_button, draw_card
from deck import Deck


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.card_font = pygame.font.Font(None, 27)
        self.HIT_BUTTON = [100, 800, 200, 100]
        self.STAND_BUTTON = [500, 800, 200, 100]
        self.RESET_BUTTON = [500, 0, 200, 100]
        self.deck = Deck()
        self.player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.game_over = False

    def is_button_clicked(self, button, mouse_pos):
        return (button[0] <= mouse_pos[0] <= (button[0] + button[2]) and
                button[1] <= mouse_pos[1] <= (button[1] + button[3]))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    if self.is_button_clicked(self.HIT_BUTTON, event.pos):
                        self.player_hand.append(self.deck.deal_card())
                    elif self.is_button_clicked(self.STAND_BUTTON, event.pos):
                        while self.calculate_total(self.dealer_hand) < 17:
                            self.dealer_hand.append(self.deck.deal_card())
                        self.game_over = True
                if self.game_over:
                    if self.is_button_clicked(self.RESET_BUTTON, event.pos):
                        self.reset_game()
        return True

    def update(self):
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        # Check for game over conditions
        if player_total > 21 or dealer_total > 21 or player_total == 21 or dealer_total == 21:
            self.game_over = True

    def draw(self):
        self.screen.fill((0, 255, 0))
        draw_text(self.screen, self.font, f"Player's hand:  {
                  self.calculate_total(self.player_hand)}", 100, 100)
        for i, card in enumerate(self.player_hand):
            draw_card(self.screen, self.card_font, card, 100 + i * 110, 150)
        draw_text(self.screen, self.font, f"Dealer's hand:   {
                  self.calculate_total(self.dealer_hand)}", 100, 300)
        for i, card in enumerate(self.dealer_hand):
            draw_card(self.screen, self.card_font, card, 100 + i * 110, 350)
        draw_button(self.screen, self.font, "Hit", *self.HIT_BUTTON)
        draw_button(self.screen, self.font, "Stand", *self.STAND_BUTTON)

        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        if self.game_over:
            if player_total > 21:
                draw_text(self.screen, self.font,
                          "Player busts! Dealer wins!", 0, 0)
            elif dealer_total > 21:
                draw_text(self.screen, self.font,
                          "Dealer busts! Player wins!", 0, 0)
            elif player_total == 21:
                draw_text(self.screen, self.font, "Player wins!", 0, 0)
            elif dealer_total == 21:
                draw_text(self.screen, self.font, "Dealer wins!", 0, 0)
            # Draw button to deal new hand
            draw_button(self.screen, self.font,
                        "Deal Again", *self.RESET_BUTTON)

        pygame.display.flip()

    def calculate_total(self, hand):
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

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.game_over = False
