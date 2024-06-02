import pygame
from ui import draw_text, draw_button, draw_card, draw_hidden_card
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
        self.player_balance = 100
        self.current_bet = 0
        self.BET_1_BUTTON = [100, 600, 200, 50]
        self.BET_10_BUTTON = [350, 600, 200, 50]
        self.BET_25_BUTTON = [100, 675, 200, 50]
        self.BET_50_BUTTON = [350, 675, 200, 50]
        self.bet_paid = False
        self.win_status = None

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
                    elif self.is_button_clicked(self.BET_1_BUTTON, event.pos):
                        self.place_bet(1)
                    elif self.is_button_clicked(self.BET_10_BUTTON, event.pos):
                        self.place_bet(10)
                    elif self.is_button_clicked(self.BET_25_BUTTON, event.pos):
                        self.place_bet(25)
                    elif self.is_button_clicked(self.BET_50_BUTTON, event.pos):
                        self.place_bet(50)

                if self.game_over:
                    if self.is_button_clicked(self.RESET_BUTTON, event.pos):
                        self.new_deal()
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

        # Draw player's hand
        for i, card in enumerate(self.player_hand):
            draw_card(self.screen, self.card_font, card, 100 + i * 110, 150)

        # Draw dealer's hand
        if self.game_over:
            for i, card in enumerate(self.dealer_hand):
                draw_card(self.screen, self.card_font,
                          card, 100 + i * 110, 350)
                draw_text(self.screen, self.font, f"Dealer's hand:   {
                    self.calculate_total(self.dealer_hand)}", 100, 300)

        else:
            draw_card(self.screen, self.card_font,
                      self.dealer_hand[0], 100, 350)
            draw_hidden_card(self.screen, self.card_font, 210, 350)
            draw_text(self.screen, self.font, f"Dealer's hand:   {
                self.calculate_total(self.dealer_hand[:1])} + ?", 100, 300)

        draw_button(self.screen, self.font, "Hit", *self.HIT_BUTTON)
        draw_button(self.screen, self.font, "Stand", *self.STAND_BUTTON)
        draw_button(self.screen, self.font, "Bet $1", *self.BET_1_BUTTON)
        draw_button(self.screen, self.font, "Bet $10", *self.BET_10_BUTTON)
        draw_button(self.screen, self.font, "Bet $25", *self.BET_25_BUTTON)
        draw_button(self.screen, self.font, "Bet $50", *self.BET_50_BUTTON)

        draw_text(self.screen, self.font, f"Current bet: ${
                  self.current_bet}", 100, 550)
        draw_text(self.screen, self.font, f"Balance: ${
                  self.player_balance}", 100, 500)

        if self.game_over:
            player_total = self.calculate_total(self.player_hand)
            dealer_total = self.calculate_total(self.dealer_hand)
            if player_total > 21:
                draw_text(self.screen, self.font,
                          "Player busts! Dealer wins!", 0, 0)
            elif dealer_total > 21:
                draw_text(self.screen, self.font,
                          "Dealer busts! Player wins!", 0, 0)
                self.win_status = "W"
            elif player_total == 21:
                draw_text(self.screen, self.font, "Player wins!", 0, 0)
                self.win_status = "W"
            elif dealer_total == 21:
                draw_text(self.screen, self.font, "Dealer wins!", 0, 0)
            elif player_total > dealer_total:
                draw_text(self.screen, self.font, "Player wins!", 0, 0)
                self.win_status = "W"
            elif dealer_total > player_total:
                draw_text(self.screen, self.font, "Dealer wins!", 0, 0)
            else:
                draw_text(self.screen, self.font, "It's a tie!", 0, 0)
                self.win_status = "T"

            # Pay out winnings
            if self.win_status == "W" and not self.bet_paid:
                self.player_balance += self.current_bet * 2
                self.bet_paid = True
            elif self.win_status == "T" and not self.bet_paid:
                self.player_balance += self.current_bet
                self.bet_paid = True

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

    def new_deal(self):
        self.deck = Deck()
        self.player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.game_over = False
        self.current_bet = 0
        self.win_status = None
        self.bet_paid = False

    def place_bet(self, amount):
        if self.player_balance >= amount:
            self.player_balance -= amount
            self.current_bet += amount
