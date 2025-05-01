from random import choice
from src.config import CellStates, STATE_COLORS, word_bank, BACKGROUND_COLOR, FONT_COLOR, Fonts

class Board:
    def __init__(self, renderer, x, rows=6, columns=5):
        self.renderer = renderer
        self.rows = rows
        self.columns = columns
        self.CELL_SIZE = 50
        self.MARGIN = 10
        self.x = x
        self.y = 120
        self.cells = [[[CellStates.EMPTY, ''] for _ in range(self.columns)] for _ in range(self.rows)]
        self.previous_cells = [[[CellStates.EMPTY, '1'] for _ in range(self.columns)] for _ in range(self.rows)]
        self.rectangles = []
        self.current_row = 0
        self.create_rectangles()
        self.word = choice(word_bank)
        self.letters_in_word = {}
        self.letters_in_word = {letter: self.word.count(letter) for letter in self.word if
                           letter not in self.letters_in_word}
        print(self.word)
        self.done = False

    def check_guess(self):
        right_letters = 0
        wrong_place_letters = []
        letters_in_word = self.letters_in_word.copy()
        for index in range(self.columns):
            letter = self.cells[self.current_row][index][1]
            if self.word[index] == letter:
                right_letters += 1
                self.cells[self.current_row][index][0] = CellStates.RIGHT
                letters_in_word[letter] -= 1
            elif letter in self.word and letters_in_word[letter] > 0:
                wrong_place_letters.append((index, letter))
            else:
                self.cells[self.current_row][index][0] = CellStates.WRONG
        for index, letter in wrong_place_letters:
            if letters_in_word[letter] > 0:
                self.cells[self.current_row][index][0] = CellStates.WRONG_PLACE
                letters_in_word[letter] -= 1
            else:
                self.cells[self.current_row][index][0] = CellStates.WRONG
        if right_letters == self.columns:
            self.done = True
        self.current_row += 1

    def place_letter(self, letter, index):
        self.cells[self.current_row][index][1] = letter

    def remove_letter(self, index):
        self.cells[self.current_row][index][1] = ''

    def create_rectangles(self):
        self.rectangles = []
        y = self.y + self.current_row * (self.CELL_SIZE + self.MARGIN)

        for index in range(len(self.cells[self.current_row])):
            x = self.x + index * (self.CELL_SIZE + self.MARGIN)
            self.rectangles.append(self.renderer.get_rect(x, y, self.CELL_SIZE, self.CELL_SIZE))

    def draw(self, current_letter_index):
        for row_idx, row in enumerate(self.cells):
            for col_idx, (state, char) in enumerate(row):
                if row_idx == self.current_row and not self.done:
                    state = CellStates.CURRENT_LINE
                elif self.cells[row_idx][col_idx] == self.previous_cells[row_idx][col_idx]:
                    continue
                x = self.x + col_idx * (self.CELL_SIZE + self.MARGIN)
                y = self.y + row_idx * (self.CELL_SIZE + self.MARGIN)

                cell_rect = self.renderer.get_rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                self.renderer.draw_rect(STATE_COLORS[state], cell_rect)

                if state == CellStates.CURRENT_LINE:
                    self.renderer.draw_rect(BACKGROUND_COLOR, cell_rect.inflate(-6, -6))
                    if col_idx == current_letter_index:
                        self.renderer.draw_rect(STATE_COLORS[state], (x, y+self.CELL_SIZE-6, self.CELL_SIZE, 6))

                if char:
                    self.renderer.draw_text(char.upper(),
                                            Fonts.BOARD,
                                            FONT_COLOR,
                                            cell_rect.center,
                                            center=True)

        self.previous_cells = [[cell[:] for cell in row] for row in self.cells]
