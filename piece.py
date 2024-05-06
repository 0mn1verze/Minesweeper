class Piece:
    def __init__(self, is_mine):
        self.is_mine = is_mine
        self.around = 0
        self.clicked = False
        self.flagged = False
        self.maybe_flagged = False
        self.neighbours = []

    def __repr__(self):
        return str(self.is_mine)

    def get_num_around(self):
        return self.around

    def has_mine(self):
        return self.is_mine

    def is_clicked(self):
        return self.clicked

    def is_flagged(self):
        return self.flagged

    def is_maybe_flagged(self):
        return self.maybe_flagged

    def toggle_flag(self):
        self.flagged = not self.flagged

    def handle_click(self):
        self.clicked = True

    def set_num_around(self):
        num = 0
        for neighbour in self.neighbours:
            if neighbour.has_mine():
                num += 1
        self.around = num

    def get_flagged_neighbour(self):
        num = 0
        for neighbour in self.neighbours:
            if neighbour.is_flagged():
                num += 1
        return num

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours
