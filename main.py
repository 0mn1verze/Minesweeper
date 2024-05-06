import pygame
import os
from piece import Piece
from board import Board


class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        self.WINDIM = 1440, 720
        self.screen = pygame.display.set_mode(self.WINDIM)
        self.piece_size = (self.WINDIM[0] / size[0], self.WINDIM[1] / size[1])
        self.load_images()

    def load_images(self):
        self.images = {}
        for file in os.listdir("./images"):
            if not file.endswith(".png"):
                continue
            path = f"./images/{file}"
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.piece_size[0]), int(self.piece_size[1])))

            self.images[file.split(".")[0]] = img

    def start(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handle_click(pygame.mouse.get_pos(), flag)
                if event.type == pygame.KEYDOWN:
                    self.board.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        dr, dc = self.piece_size
        for r, row in enumerate(self.board.get_board()):
            for p, piece in enumerate(row):
                image = self.images[self.get_img(piece)]
                self.screen.blit(image, (r * dr, p * dc))

    def get_img(self, piece):
        if piece.is_clicked():
            return str(piece.get_num_around()) if not piece.has_mine() else 'bomb-at-clicked-block'
        if self.board.lost:
            if piece.has_mine():
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.is_flagged() else 'empty-block'
        return 'flag' if piece.is_flagged() else 'maybe-flag' if piece.is_maybe_flagged() else 'empty-block'

    def handle_click(self, position, flag):
        index = tuple(int(pos // size)
                      for pos, size in zip(position, self.piece_size))
        self.board.handle_click(self.board.get_piece(index), flag, True)


if __name__ == "__main__":
    size = 60, 30
    prob = 0.15
    g = Game(size, prob)
    g.start()
