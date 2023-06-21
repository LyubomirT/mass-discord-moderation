import os
import sys

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')  # Clear screen for Windows
    else:
        os.system('clear')  # Clear screen for Unix-based systems

class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'