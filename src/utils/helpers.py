import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)

def load_word_bank(file_path):
    """Load and process the word bank from file"""
    with open(file_path, 'r') as arquivo:
        word_bank = arquivo.read().splitlines()
        return [word for word in word_bank if len(word) == 5]
