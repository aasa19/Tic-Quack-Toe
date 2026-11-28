# Libraries and frameworks
import pygame
import random

# Import files
import interface as ui
import user_input as ux
from fonts import default_font
from images import pwingu

# Play menu class
# Creates a grid for the user to play with against an AI
class PlayMenu:
    def __init__(self, window):

        # Set window
        self.window = window

        # Set scores
        self.player_score = 0
        self.bot_score = 0

        # Set turn order
        # Chooses player or bot by random when first running the program
        self.turn = random.choice(["Player", "Bot"])

        # Create attributes
        self.create_attributes()

        # Create pwingu images
        self.create_pwingu_images()

        # Create left click
        self.left_click = ux.ButtonPress("mouse", 0)

        # Set running to true by default
        # Should immediately run the game loop when run is called
        self.running = True

    # Set turn order after restarting the grid
    def set_turn_order(self):

        # Chooses player or bot by random if there was no previous winner
        # If the player or bot lost the previous round, they go first
        match self.winner:

            # Bot goes first
            case "Player":
                self.turn = "Bot"

            # Player goes first
            case "Bot":
                self.turn = "Player"

            # Choses player or bot by random
            case _:
                self.turn = random.choice(["Player", "Bot"])

    # Creates attributes
    def create_attributes(self):

        # Create grid
        self.grid = ui.Grid(self.window, self)

        # Create texts
        self.create_texts()

        # Set winner to None by default
        # Check which player or bot won
        self.winner = None

    # Creates texts
    def create_texts(self):

        # Window size
        width = self.window.width
        height = self.window.height

        # Text size
        text_size = width / 30
        description_text_size = width / 45

        # Margins
        # Distance from the left border
        turn_left_margin = width / 2
        turn_description_left_margin = turn_left_margin
        player_score_left_margin = width / 6
        bot_score_left_margin = width - player_score_left_margin
        play_again_left_margin = turn_left_margin - width / 6
        reset_left_marin = turn_left_margin + width / 6
        
        # Distance from the top border
        turn_top_margin = height / 5
        turn_description_top_margin = turn_top_margin + height / 25
        player_score_top_margin = height / 2.275
        play_again_top_margin = height * (1 - 1 / 4.5)
        reset_top_margin = play_again_top_margin

        # Create turn text
        self.turn_text = ui.Text(self.window, f"It's {self.turn}'s turn!", default_font, text_size, (0, 0, 0), turn_left_margin, turn_top_margin, "center", False)
        self.turn_description = ui.Text(self.window, "", default_font, description_text_size, (0, 0, 0), turn_description_left_margin, turn_description_top_margin, "center", False)

        # Create score texts
        self.player_score_text = ui.Text(self.window, f"Player Score: {self.player_score}", default_font, text_size, (100, 100, 200), player_score_left_margin, player_score_top_margin, "center", False)
        self.bot_score_text = ui.Text(self.window, f"Bot Score: {self.bot_score}", default_font, text_size, (200, 100, 100), bot_score_left_margin, self.player_score_text.y, "center", False)

        # Create play again and reset texts
        self.play_again_text = ui.Text(self.window, "Play Again", default_font, text_size, (50, 50, 50), play_again_left_margin, play_again_top_margin, "center", True)
        self.reset_text = ui.Text(self.window, "Reset", default_font, text_size, (50, 50, 50), reset_left_marin, reset_top_margin, "center", True)

        # Create collection of texts
        self.texts = [self.turn_text, self.turn_description, self.player_score_text, self.bot_score_text, self.play_again_text, self.reset_text]

    # Create pwingu images
    def create_pwingu_images(self):

        # Window size
        height = self.window.height

        # Margins
        # Distance from left border
        player_pwingu_left_margin = self.player_score_text.x
        bot_pwingu_left_margin = self.bot_score_text.x

        # Distance from right border
        player_pwingu_top_margin = self.player_score_text.y + height / 15
        bot_pwingu_top_margin = self.bot_score_text.y + height / 15

        # Create pwingu images
        self.player_pwingu_image = ui.PwinguImage(self.window, pwingu, (150, 150, 255), player_pwingu_left_margin, player_pwingu_top_margin, True)
        self.bot_pwingu_image = ui.PwinguImage(self.window, pwingu, (255, 150, 150), bot_pwingu_left_margin, bot_pwingu_top_margin, False)

        # Create collection of images
        self.images = [self.player_pwingu_image, self.bot_pwingu_image]

    # Runs program
    def run(self):
        # Game loop
        while self.running:

            # Update left click
            self.left_click.update()

            # Set frames per second to 60
            self.window.clock.tick(60)

            # Fills the screen in dark grey
            self.window.display.fill((255, 255, 255))

            # Event handler
            for event in pygame.event.get():

                # Exits the loop
                if event.type == pygame.QUIT:
                    self.running = False

            # Updates turn text based on certain conditions
            match self.winner:

                # Checks if there is a winner
                case winner if winner:

                    # Change texts
                    self.turn_text.text = f"{self.winner} won!"
                    self.turn_description.text = f"Would you like to play again?"

                    # Set play again text to active when the player or bot wins
                    self.play_again_text.active = True

                # Checks if there are no winners
                case winner if not winner:

                    # Checks if there are any available squares
                    # If all squares are occupied, neither player or bot wins
                    if len([square for square in self.grid.squares if square.chosen]) == 9:
                        self.turn_text.text = f"Tie!"
                        self.turn_description.text = "Would you like to play again?"

                        # Set play again text to active when there is a tie
                        self.play_again_text.active = True

                    else:

                        # Change text to whose turn it is
                        self.turn_text.text = f"It's {self.turn}'s turn!"

                        # Change description text if it's the player or bot's turn
                        if self.turn == "Player":
                            self.turn_description.text = f"Choose a square you would like to place your Pwingu at."

                        elif self.turn == "Bot":
                            self.turn_description.text = f"{self.turn} is thinking..."

                        # Set play again text to inactive
                        self.play_again_text.active = False

            # Update score texts
            self.player_score_text.text = f"Player Score: {self.player_score}"
            self.bot_score_text.text = f"Bot Score: {self.bot_score}"

            # Checks if any grid squares have been chosen
            if any([square for square in self.grid.squares if square.chosen]):

                # Set reset text to active
                self.reset_text.active = True

            # Checks if play again text has been clicked on
            if self.play_again_text.highlighted and self.left_click.action:

                # Set turn order for next round
                self.set_turn_order()

                # Restart screen
                self.create_attributes()

                # Set reset test to active
                self.reset_text.active = True

            # Checks if reset text has been clicked on
            if self.reset_text.highlighted and self.left_click.action:

                # Chooses player or bot by random when resetting the program
                self.turn = random.choice(["Player", "Bot"])

                # Reset scores
                self.player_score = 0
                self.bot_score = 0

                # Restart screen
                self.create_attributes()

                # Set reset text to inactive
                self.reset_text.active = False

            # Draw images
            for image in self.images:
                image.draw()

            # Draw texts
            for text in self.texts:
                text.draw()

            # Draw grid
            self.grid.draw()

            # Update window
            pygame.display.flip()
