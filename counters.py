# Counter class
# Creates a counter that outputs a result after meeting a threshold
class Counter:
    def __init__(self, threshold):

        # Set counter to 0 by default
        # Counter should start at 0 when first created
        self.counter = 0

        # Set threshold
        self.threshold = threshold

        # Set action to false by default
        # Should only be true when the counter is greater than or equal to the given threshold
        # Used to signal to other functions or classes outside this scope
        self.action = False

    # Updates and increments counter per tick
    def update(self):

        # Set action to false per iteration
        self.action = False

        # Checks if counter is greater than or equal to its threshold
        if self.counter >= self.threshold:

            # Reset counter
            self.counter = 0

            # Set action to true
            # Tells other functions or classes that the threshold has been reached
            self.action = True

        # Increment counter by 1
        else:

            self.counter += 1