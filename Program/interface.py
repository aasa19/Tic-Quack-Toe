# Libraries and frameworks
import pygame
import random

# Import files
import counters
from images import grid_square, pwingu
from sounds import victory, fail

# Window class
# Creates a window for display
class Window:
    def __init__(self):

        # Window size
        # self.width = pygame.display.Info().current_w - 10
        # self.height = pygame.display.Info().current_h - 60
        self.width = 750
        self.height = 750

        # Create window
        self.display = pygame.display.set_mode((self.width, self.height))

        # Window name
        pygame.display.set_caption("Tic-Quack-Toe")

        # Create clock
        self.clock = pygame.Clock()

        # Set window icon
        pygame.display.set_icon(pygame.image.load(pwingu))

# Text class
# Creates text
class Text:
    def __init__(self, window, text, font_file, font_size, color, x, y, alignment, interactive):

        # Set attributes
        self.window = window
        self.text = text

        # Create font using font file
        self.font = pygame.font.Font(font_file)

        # Set font size
        self.font.set_point_size(int(font_size))

        # Set initial color and color
        # Initial color is used as the base color
        # Color is used to alter the color during runtime
        self.initial_color = color
        self.color = self.initial_color

        # Set coordinates
        self.x = x
        self.y = y

        # Set alignment
        self.alignment = alignment

        # Set interacive
        self.interactive = interactive

        # Creates additional attributes if interactive
        if self.interactive:

            # Set highlighted to false by default
            self.highlighted = False

            # Set active to false by default
            self.active = False

        # Creates text
        self.create_text()

    # Creates highlight effect
    def highlight(self):

         # Mouse position
        mouse = pygame.mouse.get_pos()
        
        # Checks if the mouse is hovering over the image
        self.highlighted = self.rect.collidepoint(mouse)
        
        # Checks if the user is hovering and if the square has not been chosen
        if self.highlighted:
        
            # Highlights image
            self.color = tuple([min(color_value + 100, 255) for color_value in self.initial_color])

        else:

            # Keeps the color as is
            self.color = tuple([min(color_value + 50, 255) for color_value in self.initial_color])

    # Creates text
    def create_text(self):

        # Create text image
        self.text_image = self.font.render(self.text, True, self.color)

        # Create text rectangle
        self.rect = self.text_image.get_rect()

        # Set alignment
        match self.alignment:

            # Aligns text to the left
            case "left":
                self.rect.left = self.x
                self.rect.y = self.y

            # Aligns text to the center
            case "center":
                self.rect.center = (self.x, self.y)

            # Aligns text to the right
            case "right":
                self.rect.right = self.x
                self.rect.y = self.y

    # Updates and draws text
    def draw(self):

        # Checks if interactive and active
        if self.interactive and self.active:

            # Create highlight effect
            self.highlight()

        # Checks if interactive
        elif self.interactive:

            self.color = self.initial_color

        # Creates/updates text
        self.create_text()

        # Draw text onto window display
        self.window.display.blit(self.text_image, self.rect)

# Pwingu image class
# Creates pwingu images
class PwinguImage:
    def __init__(self, window, image_file, color, x, y, flip_horizontally):

        # Set attributes
        self.window = window
        self.image_file = image_file

        # Set color
        self.color = color

        # Set coordinates
        self.x = x
        self.y = y

        # Set flip horizontally
        # Flips the image horizontally when true
        self.flip_horizontally = flip_horizontally

        # Create image
        self.create_image()

    # Creates image
    def create_image(self):

        # Create image
        self.initial_image = pygame.image.load(self.image_file)

        # Checks if flip is true
        if self.flip_horizontally:

            # Flip image
            self.image = pygame.transform.flip(self.initial_image, True, False)

        else:

            # Set image to initial image
            self.image = self.initial_image

        # Create image surface (hitbox)
        self.rect = self.image.get_rect()
        
        # Center image origin
        self.rect.center = (self.x, self.y)

    # Draws and updates image
    def draw(self):

        # Updates image
        self.create_image()

        # Change color
        self.image.fill(self.color, special_flags = pygame.BLEND_MULT)

        # Draw image
        self.window.display.blit(self.image, self.rect)

# Square class
# Creates grid squares
class Square:
    def __init__(self, window, image_file, color, x, y):

        # Set attributes
        self.window = window
        self.image_file = image_file

        # Set initial color
        self.initial_color = color
        self.color = self.initial_color

        # Set coordinates
        self.x = x
        self.y = y

        # Create image 
        self.create_image()

        # Set chosen to false by default
        # Used to check if the square is chosen or not
        self.chosen = False

        # Set both player and bot to false
        # Checks which squares are chosen by the player or bot
        self.chosen_by_player = False
        self.chosen_by_bot = False

    # Creates image
    def create_image(self):

        # Create image
        self.image = pygame.image.load(self.image_file)

        # Create image surface (hitbox)
        self.rect = self.image.get_rect()

        # Center image origin
        self.rect.center = (self.x, self.y)

    # Creates a highlight effect
    def highlight(self):

        # Mouse position
        mouse = pygame.mouse.get_pos()

        # Checks if the mouse is hovering over the image
        self.highlighted = self.rect.collidepoint(mouse)

        # Checks if the user is hovering and if the square has not been chosen
        if self.highlighted and not self.chosen:

            # Highlights image
            self.color = tuple([min(color_value + 55, 255) for color_value in self.initial_color])

        # Checks if not chosen
        elif not self.chosen:

            # Keeps color as is
            self.color = self.initial_color

    # Updates and draws image
    def draw(self):

        # Updates image
        self.create_image()

        # Change color
        self.image.fill(self.color, special_flags = pygame.BLEND_MULT)

        # Draw image
        self.window.display.blit(self.image, self.rect)

        # Draw pwingu when chosen
        if self.chosen:

            # Change color of pwingu if chosen by player or bot
            if self.chosen_by_player:

                # Create red pwingu image
                self.pwingu = PwinguImage(self.window, pwingu, (150, 150, 255), self.x, self.y, True)

            elif self.chosen_by_bot:

                # Create blue pwingu image
                self.pwingu = PwinguImage(self.window, pwingu, (255, 150, 150), self.x, self.y, False)

            # Change pwingu color
            self.pwingu.image.fill(self.color, special_flags = pygame.BLEND_MULT)
            self.pwingu.draw()

# Grid class
# Creates a grid of interactive squares
class Grid:
    def __init__(self, window, program):

        # Set attributes
        self.window = window
        self.program = program

        # Create bot counter
        # Creates pauses before each bot's turn
        self.bot_counter = counters.Counter(30)

        # Create grid
        self.create_grid()

    # Creates grid
    def create_grid(self):

        # Distance from middle square vertically
        vertical_middle_square_margin = 77.5

        # Distance from middle square horizontally
        horizontal_middle_square_margin = 77.5

        # Create squares

        # Top squares
        self.top_left_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 - horizontal_middle_square_margin, self.window.height / 2 - vertical_middle_square_margin)
        self.top_middle_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2, self.window.height / 2 - vertical_middle_square_margin)
        self.top_right_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 + horizontal_middle_square_margin, self.window.height / 2 - vertical_middle_square_margin)
        self.top_squares = [self.top_left_square, self.top_middle_square, self.top_right_square]

        # Middle squares
        self.left_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 - horizontal_middle_square_margin, self.window.height / 2)
        self.middle_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2, self.window.height / 2)
        self.right_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 + horizontal_middle_square_margin, self.window.height / 2)
        self.middle_squares = [self.left_square, self.middle_square, self.right_square]

        # Bottom squares
        self.bottom_left_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 - horizontal_middle_square_margin, self.window.height / 2 + vertical_middle_square_margin)
        self.bottom_middle_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2, self.window.height / 2 + vertical_middle_square_margin)
        self.bottom_right_square = Square(self.window, grid_square, (200, 200, 200), self.window.width / 2 + horizontal_middle_square_margin, self.window.height / 2 + vertical_middle_square_margin)
        self.bottom_squares = [self.bottom_left_square, self.bottom_middle_square, self.bottom_right_square]

        # Combines squares into a single collection
        self.squares = self.top_squares + self.middle_squares + self.bottom_squares

        # Combines collections of squares into a single collection by row
        self.rows = [self.top_squares] + [self.middle_squares] + [self.bottom_squares]

        # Combines collections of squares into a single collection by column
        self.columns = [[self.top_left_square, self.left_square, self.bottom_left_square], [self.top_middle_square, self.middle_square, self.bottom_middle_square], [self.top_right_square, self.right_square, self.bottom_right_square]]

        # Combines collections of squares into a single collection by diagonals
        self.diagonals = [[self.top_left_square, self.middle_square, self.bottom_right_square], [self.bottom_left_square, self.middle_square, self.top_right_square]]

        # Combines rows, columns, and diagonals into a single collection
        self.variations = [self.rows, self.columns, self.diagonals]

    # Create turn order
    def turn_order(self):

        # Checks which turn it is
        match self.program.turn:

            # Player's turn
            case "Player":

                # Iterates through each square
                for square in self.base_squares:

                    # Creates highlight effect when hovering over a square
                    square.highlight()

                    # Checks if the user left-clicked and if square is being hovered
                    if self.program.left_click.action and square.highlighted:

                        # Change square color
                        square.color = (150, 150, 255)

                        # Set selected square chosen to true
                        square.chosen = True
                        square.chosen_by_player = True

                        # Switch turn to bot
                        self.program.turn = "Bot"

                        # Break out of current loop
                        break

            # Bot's turn
            case "Bot":

                # Update bot counter
                self.bot_counter.update()

                # Checks if the bot counter reached its threshold
                if self.bot_counter.action:
                    
                    # Chooses a random square to highlight
                    random_square = random.choice(self.base_squares)

                    # Change square color
                    random_square.color = (255, 150, 150)

                    # Set random square chosen to true
                    random_square.chosen = True
                    random_square.chosen_by_bot = True

                    # Switch turn to player
                    self.program.turn = "Player"

    # Checks for win conditions
    def check_win_conditions(self):

        # Iterates through each variation
        for variation in self.variations:
        
            # Iterates through each square
            for squares in variation:
        
                # Checks if all squares are chosen by player
                if len([square for square in squares if square.chosen_by_player]) == 3:
        
                    # Brighten color after getting 3 in a row
                    for square in squares: 
                        square.color = (205, 205, 255)
        
                        # Checks if there is no winner
                        if not self.program.winner:
        
                            # Plays a victory sound
                            pygame.mixer.Sound(victory).play()
        
                            # Set winner to player
                            self.program.winner = "Player"
        
                            # Increment player score
                            self.program.player_score += 1
        
                # Checks if all squares are chosen by bot
                elif len([square for square in squares if square.chosen_by_bot]) == 3:
        
                    # Brighten color after getting 3 in a row
                    for square in squares: 
                        square.color = (255, 205, 205)
        
                        # Checks if there is no winner
                        if not self.program.winner:
        
                            # Plays a fail sound
                            pygame.mixer.Sound(fail).play()
        
                            # Set winner to bot
                            self.program.winner = "Bot"
        
                            # Increment bot score
                            self.program.bot_score += 1

    # Draw grid
    def draw(self):

        # Updates and draws each square
        for square in self.squares:

            # Draw square
            square.draw()

        # Filters out squares that were chosen
        self.base_squares = [square for square in self.squares if not square.chosen]

        # Filters out squares that weren't chosen
        self.chosen_squares = [square for square in self.squares if square.chosen]

        # Checks if there are only chosen squares and not a winner
        if any(self.base_squares) and not self.program.winner:

            # Get turn order
            self.turn_order()

        # Checks if there is no winner
        if not self.program.winner:

            # Checks win conditions whether the player or bot wins
            self.check_win_conditions()
