import pygame
from ui import draw_text, draw_button, draw_card, draw_hidden_card, draw_menu_card
from deck import Deck


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.MAIN_MENU_BUTTON = [300, 300, 200, 100]
        self.PLAY_BUTTON = [400, 550, 200, 100]
        self.QUIT_BUTTON = [725, 550, 200, 100]
        self.show_main_menu = True
        self.font = pygame.font.Font(None, 50)
        self.card_font = pygame.font.Font(None, 27)
        self.menu_card_font = pygame.font.Font(None, 41)
        self.menu_font = pygame.font.Font(None, 100)
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
        self.EXIT_TO_MAIN_MENU_BUTTON = [750, 0, 250, 100]
        self.CONFIRM_BUTTON = [300, 300, 200, 100]
        self.CANCEL_BUTTON = [750, 300, 200, 100]
        self.show_reset_prompt = False
        self.show_main_menu = True
        self.DEAL_BUTTON = [400, 400, 200, 100]
        self.deal_button_clicked = False

    def is_button_clicked(self, button, mouse_pos):
        return (button[0] <= mouse_pos[0] <= (button[0] + button[2]) and
                button[1] <= mouse_pos[1] <= (button[1] + button[3]))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Main menu
                if self.show_main_menu:
                    if self.is_button_clicked(self.PLAY_BUTTON, event.pos):
                        self.show_main_menu = False
                        self.reset_game()
                    elif self.is_button_clicked(self.QUIT_BUTTON, event.pos):
                        return False
                # Get bets
                elif not self.deal_button_clicked:
                    if self.is_button_clicked(self.BET_1_BUTTON, event.pos):
                        self.place_bet(1)
                    if self.is_button_clicked(self.BET_10_BUTTON, event.pos):
                        self.place_bet(10)
                    if self.is_button_clicked(self.BET_25_BUTTON, event.pos):
                        self.place_bet(25)
                    if self.is_button_clicked(self.BET_50_BUTTON, event.pos):
                        self.place_bet(50)

                    if self.is_button_clicked(self.DEAL_BUTTON, event.pos):
                        self.deal_button_clicked = True
                        self.player_hand = [
                            self.deck.deal_card(), self.deck.deal_card()]
                        self.dealer_hand = [
                            self.deck.deal_card(), self.deck.deal_card()]
                    self.handle_exit_to_main_menu(event)
                # Game in progress
                elif not self.game_over:
                    if self.is_button_clicked(self.HIT_BUTTON, event.pos):
                        self.player_hand.append(self.deck.deal_card())
                    if self.is_button_clicked(self.STAND_BUTTON, event.pos):
                        while self.calculate_total(self.dealer_hand) < 17:
                            self.dealer_hand.append(self.deck.deal_card())
                        self.game_over = True
                    self.handle_exit_to_main_menu(event)

                if self.game_over:
                    if self.is_button_clicked(self.RESET_BUTTON, event.pos):
                        self.new_deal()
                    self.handle_exit_to_main_menu(event)
        return True

    def handle_exit_to_main_menu(self, event):
        if self.is_button_clicked(self.EXIT_TO_MAIN_MENU_BUTTON, event.pos):
            self.show_reset_prompt = True
        if self.show_reset_prompt:
            if self.is_button_clicked(self.CONFIRM_BUTTON, event.pos):
                self.show_main_menu = True
                self.show_reset_prompt = False
            elif self.is_button_clicked(self.CANCEL_BUTTON, event.pos):
                self.show_reset_prompt = False

    def update(self):
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        # Check for game over conditions
        if player_total > 21 or dealer_total > 21 or player_total == 21 or dealer_total == 21:
            self.game_over = True

    def draw(self):
        if self.show_main_menu:
            self.screen.fill((0, 255, 0))

            # Draw background
            pygame.draw.rect(self.screen, (0, 0, 0), (180, 180, 960, 520))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (200, 200, 920, 480))

            # Draw Ace cards
            aces = [("Ace", "Hearts", "A"), ("Ace", "Clubs", "A"),
                    ("Ace", "Diamonds", "A"), ("Ace", "Spades", "A")]
            for i, ace in enumerate(aces):
                draw_menu_card(self.screen, self.menu_card_font,
                               ace, 250 + i * 150 * 1.5, 300)

            # Draw main menu buttons
            draw_text(self.screen, self.menu_font, "Blackjack", 500, 210)
            draw_button(self.screen, self.font, "Play", *self.PLAY_BUTTON)
            draw_button(self.screen, self.font, "Quit", *self.QUIT_BUTTON)
        else:
            self.screen.fill((0, 255, 0))
            draw_text(self.screen, self.font, f"Player's hand:  {
                      self.calculate_total(self.player_hand)}", 100, 100)

            # Draw deal button
            if not self.deal_button_clicked:
                draw_button(self.screen, self.font, "Deal", *self.DEAL_BUTTON)
            else:

                # Draw player's hand
                for i, card in enumerate(self.player_hand):
                    draw_card(self.screen, self.card_font,
                              card, 100 + i * 110, 150)

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

            # Draw reset game button
            draw_button(self.screen, self.font, "Main Menu",
                        *self.EXIT_TO_MAIN_MENU_BUTTON)
            if self.show_reset_prompt:
                pygame.draw.rect(self.screen, (0, 0, 0), (180, 180, 940, 320))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (200, 200, 900, 280))
                draw_text(self.screen, self.font,
                          "Are you sure you want to exit to the Main Menu?", 250, 250)
                draw_button(self.screen, self.font, "Yes",
                            *self.CONFIRM_BUTTON)
                draw_button(self.screen, self.font, "No",
                            *self.CANCEL_BUTTON)

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
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.current_bet = 0
        self.win_status = None
        self.bet_paid = False
        self.deal_button_clicked = False

    def reset_game(self):
        self.player_balance = 100
        self.new_deal()

    def place_bet(self, amount):
        if self.player_balance >= amount:
            self.player_balance -= amount
            self.current_bet += amount
