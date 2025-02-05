import random
import pygame

pygame.init()

RESOLUTION = (480, 270)
BACKGROUND_COLOR = 'black'
MAX_FPS = 20


class Field:
    grid_color = 'white'
    grid_width = 2
    piece_shrink = .8

    def __init__(self, screen, rows: int = 5, columns: int = 4):
        self.rows = rows
        self.columns = columns
        self.sel_start = None
        self.surface = screen

        self.cell_size = (min(self.surface.get_size()) - self.grid_width * (max(self.rows, self.columns) + 1)) // max(self.rows, self.columns)
        self.piece_size = self.cell_size * self.piece_shrink
        self.clock = pygame.time.Clock()

        self.piece_types = [
            Circle(self.piece_size),
            Square(self.piece_size),
            Triangle(self.piece_size),
        ]

        self.generate_pieces()

    def generate_pieces(self):
        self._pieces = [[None] * self.columns for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.columns):
                random.shuffle(self.piece_types)
                for piece in self.piece_types:
                    if self.is_valid(row, col, piece):
                        self._pieces[row][col] = piece
                        print(piece, end=' ')
                        break
            print()
        return self._pieces

    def is_valid(self, row: int, col: int, piece: 'Piece'):
        if col >= 2 and self._pieces[row][col - 1] == piece and self._pieces[row][col - 2] == piece:
            return False

        if row >= 2 and self._pieces[row - 1][col] == piece and self._pieces[row - 2][col] == piece:
            return False
        return True

    def run(self):

        while True:
            while (event := pygame.event.poll()):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                if (
                    (event.type == pygame.MOUSEBUTTONUP)
                    and (event.button == 1)
                ):
                    x, y = event.pos

                    if self.sel_start:
                        self.sel_end = (y // self.cell_size, x // self.cell_size)
                        if (self.sel_end[0] >= self.rows) or (self.sel_end[1] >= self.columns) or (self.sel_end[0] < 0) or (self.sel_end[1] < 0):
                            self.sel_end = None
                        self.turn()
                        self.sel_start = self.sel_end = None
                    else:
                        self.sel_start = (y // self.cell_size, x // self.cell_size)
                        if (self.sel_start[0] >= self.rows) or (self.sel_start[1] >= self.columns) or (self.sel_start[0] < 0) or (self.sel_start[1] < 0):
                            self.sel_start = None

            self.draw()
            self.clock.tick(MAX_FPS)

    def turn(self):
        rs, cs = self.sel_start
        re, ce = self.sel_end
        if (
            abs(rs - re) > 1
            or abs(cs - ce) > 1
            or (abs(rs - re) == 1 and abs(ce - cs) == 1)
        ):
            return

        self._pieces[rs][cs], self._pieces[re][ce] = self._pieces[re][ce], self._pieces[rs][cs]
        while self.blow():
            self.fill_field()

    def blow(self):
        is_blowed = False
        k = 3
        for i in range(self.rows):
            for j in range(self.columns - 2):
                if len(set(self._pieces[i][j:j + k])) == 1:
                    self._pieces[i][j:j + k] = [Empty(self.piece_size)] * k
                    is_blowed = True
        for i in range(self.rows - 2):
            for j in range(self.columns):
                temp = set()
                for n in range(k):
                    temp.add(self._pieces[i + n][j])
                if len(temp) == 1:
                    for n in range(k):
                        self._pieces[i + n][j] = Empty(self.piece_size)
                        is_blowed = True
        return is_blowed

    def fill_field(self):
        # gravitaion
        for now_row in reversed(range(self.rows)):
            for col in range(self.columns):
                if self._pieces[now_row][col]:
                    continue
                for grav_row in reversed(range(now_row)):
                    if self._pieces[grav_row][col]:
                        self._pieces[now_row][col], self._pieces[grav_row][col] = self._pieces[grav_row][col], Empty(self.piece_size)
                        break
        # filling with new pieces
        for row in range(self.rows):
            for col in range(self.columns):
                if not self._pieces[row][col]:
                    self._pieces[row][col] = random.choice(self.piece_types)

    def draw(self, dest=(0, 0)):
        self.surface.fill(BACKGROUND_COLOR)
        # horizontal lines
        for i in range(self.rows + 1):
            pygame.draw.line(
                self.surface, self.grid_color,
                (0, i * self.cell_size), (self.columns * self.cell_size, i * self.cell_size),
                self.grid_width
            )
        # vertical lines
        for i in range(self.columns + 1):
            pygame.draw.line(
                self.surface, self.grid_color,
                (i * self.cell_size, 0), (i * self.cell_size, self.rows * self.cell_size),
                self.grid_width
            )
        # pieces
        shift = (self.cell_size - self.piece_size) // 2
        for i in range(self.rows):
            y = i * self.cell_size + shift
            for j in range(self.columns):
                x = j * self.cell_size + shift
                self._pieces[i][j].draw(self.surface, (x, y))

        # selected piece

        pygame.display.update()


class Piece:
    color = 'white'
    name = 'piece'

    def __init__(self, size, background_color=BACKGROUND_COLOR):
        self.surface = pygame.surface.Surface((size, size))
        self.surface.set_colorkey(background_color)
        self.surface.fill(background_color)

    def __eq__(self, other):
        return isinstance(self, type(other))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return True

    def draw(self, screen, center):
        screen.blit(self.surface, center)


class Square(Piece):
    color = 'red'
    name = 'square'

    def __init__(self, size, background_color=BACKGROUND_COLOR):
        super().__init__(size, background_color)
        pygame.draw.rect(
            self.surface, self.color,
            (0, 0, size, size),
        )


class Circle(Piece):
    color = 'green'
    name = 'circle'

    def __init__(self, size, background_color=BACKGROUND_COLOR):
        super().__init__(size, background_color)

        pygame.draw.circle(
            self.surface, self.color,
            (size // 2, size // 2), size // 2
        )


class Triangle(Piece):
    color = 'blue'
    name = 'triangle'

    def __init__(self, size, background_color=BACKGROUND_COLOR):
        super().__init__(size, background_color)

        pygame.draw.polygon(
            self.surface, self.color,
            ((0, size), (size // 2, 0), (size, size)),
        )


class Empty(Piece):
    color = 'black'
    name = 'empty'

    def __init__(self, size, background_color=BACKGROUND_COLOR):
        super().__init__(size, background_color)

        pygame.draw.rect(
            self.surface, self.color,
            (0, 0, size, size),
        )

    def __bool__(self):
        return False


def main():
    # info = pygame.display.Info()
    screen = pygame.display.set_mode(RESOLUTION)
    Field(screen).run()


if __name__ == '__main__':
    main()

pygame.quit()
