# Libraries and frameworks
import pygame

# Import files
import interface as ui
import screens

# Completed
    # Created the grid
    # Finish round after the player or bot gets a succession
    # Created a restart button
    # Created player scores
    # Create x's and o's instead of making the text red or blue
    # Indicate whose turn it is
    # Create a play again button
    # Fixed an issue where the reset text would flash black when playing again

# Initialize pygame
pygame.init()

# Create window
window = ui.Window()
play_menu = screens.PlayMenu(window)

# Run play menu
play_menu.run()

# Close program
pygame.quit() 
