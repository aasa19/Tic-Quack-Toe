# Libraries and frameworks
import os

# Returns a file by finding its path
def get_path(folder, file):
    root_path = os.path.dirname(__file__)
    return os.path.join(root_path, folder, file)