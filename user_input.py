# Libraries and frameworks
import pygame

# Button press class
# Creates an key/mouse input that outputs
class ButtonPress:
    def __init__(self, button_type, selected_button):

        # Set button type
        self.button_type = button_type

        # Set selected button
        self.selected_button = selected_button

        # Set pressed to false by default
        # Checks whether the button was pressed or not
        self.pressed = False

        # Set action to false by default
        # Creates interactions with functions and classes outside of this scope
        self.action = False

    # Update buttons
    def update(self):

        # Set buttons
        match self.button_type:

            # Mouse presses
            case "mouse":
                self.buttons = pygame.mouse.get_pressed()

            # Key presses
            case "key":
                self.buttons = pygame.key.get_pressed()

        # Resets action per iteration
        self.action = False

        # Checks if the selected button was pressed and was not previously pressed
        if self.buttons[self.selected_button] and not self.pressed:

            # Set pressed to true
            # Outputs only once, not multiple instances
            self.pressed = True

            # Set action to true
            # Used as an output for functions and classes outside of this scope
            self.action = True

        # Checks if the selected button was not pressed
        if not self.buttons[self.selected_button]:

            # Set pressed to true
            self.pressed = False