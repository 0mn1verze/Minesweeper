from random import random, randint, choice
from piece import Piece


class Board:
    def __init__(self, size, prob):
        self.size = size
        self.board = []
        self.clicked = []
        self.lost = False
        for row in range(size[0]):
            row = []
            for _ in range(size[1]):
                bomb = random() < prob
                piece = Piece(bomb)
                row.append(piece)
            self.board.append(row)
        self.set_neighbours()
        self.set_num_around()

    def __str__(self):
        return "\n".join(" ".join(row) for row in self.board)

    def get_board(self):
        return self.board

    def get_size(self):
        return self.size

    def get_piece(self, index):
        return self.board[index[0]][index[1]]

    def handle_click(self, piece, flag, recurse):
        if self.lost:
            return
        if piece.is_clicked():
            if not recurse or piece.is_flagged() and not flag:
                return
            if piece.get_flagged_neighbour() - piece.around == 0 and piece.around > 0:
                for neighbour in piece.neighbours:
                    if not neighbour.is_flagged():
                        neighbour.handle_click()
                        if neighbour.get_num_around() > 0:
                            self.clicked.append(neighbour)
        if flag:
            piece.toggle_flag()
            return
        piece.handle_click()
        if piece.has_mine():
            self.lost = True
            return
        if piece.get_num_around() > 0:
            self.clicked.append(piece)
        if piece.get_num_around() == 0:
            for neighbour in piece.neighbours:
                self.handle_click(neighbour, False, False)

    def set_neighbours(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.board[row][col]
                neighbours = []
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        r = row + dr
                        c = col + dc
                        if r < 0 or r >= self.size[0]:
                            continue
                        if c < 0 or c >= self.size[1]:
                            continue
                        neighbours.append(self.board[r][c])
                piece.set_neighbours(neighbours)

    def set_num_around(self):
        for row in self.board:
            for piece in row:
                piece.set_num_around()

    def move(self):
        changed = False
        if not self.clicked:
            row = randint(0, self.size[0] - 1)
            col = randint(0, self.size[1] - 1)
            piece = self.get_piece((row, col))
            self.handle_click(piece, False, True)
            changed = True
        else:
            for piece in self.clicked:
                unknown = []
                flagged = 0
                for neighbour in piece.neighbours:
                    if neighbour.is_flagged():
                        flagged += 1
                        continue
                    if neighbour.is_clicked():
                        continue
                    unknown.append(neighbour)
                if len(unknown) + flagged == piece.around:
                    changed = True
                    for neighbour in unknown:
                        neighbour.toggle_flag()
                elif flagged == piece.around:
                    changed = True
                    for neighbour in unknown:
                        neighbour.handle_click()
                        self.clicked.append(neighbour)
        if not changed:
            row = randint(0, self.size[0] - 1)
            col = randint(0, self.size[1] - 1)
            piece = self.get_piece((row, col))
            self.handle_click(piece, False, True)
            changed = True
