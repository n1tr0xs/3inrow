import random
import pygame

pygame.init()

RESOLUTION = (1920, 1080)
BACKGROUND_COLOR = 'black'
MAX_FPS = 20


class Field:
    grid_color = 'white'
    grid_width = 2
    piece_shrink = .8

    def __init__(self, screen, rows: int = 5, columns: int = 4):
        self.rows = rows
        self.columns = columns

        self.surface = screen

        self.cell_size = (min(self.surface.get_size()) - self.grid_width * (max(self.rows, self.columns) + 1)) // max(self.rows, self.columns)
        self.piece_size = self.cell_size * self.piece_shrink
        self.clock = pygame.time.Clock()
        self.generate_pieces()

    def generate_pieces(self):
        pieces = [
            Circle(self.piece_size),
            Square(self.piece_size),
            Triangle(self.piece_size),
        ]

        self._pieces = [[None] * self.columns for i in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.columns):
                random.shuffle(pieces)
                for piece in pieces:
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
        column_start = row_start = column_end = row_end = None
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
                    if column_start:
                        column_end, row_end = x // self.cell_size, y // self.cell_size
                        self.turn(row_start, column_start, row_end, column_end)
                        column_start = row_start = column_end = row_end = None
                    else:
                        column_start, row_start = x // self.cell_size, y // self.cell_size

            self.draw()
            self.clock.tick(MAX_FPS)

    def turn(self, rs, cs, re, ce):
        if abs(re - rs) > 1:
            return
        if abs(ce - cs) > 1:
            return
        if abs(ce - cs) == 1 and abs(re - rs) == 1:
            return
        if self.rows <= rs < 0:
            return
        if self.rows <= re < 0:
            return
        if self.columns <= cs < 0:
            return
        if self.columns <= ce < 0:
            return

        self._pieces[rs][cs], self._pieces[re][ce] = self._pieces[re][ce], self._pieces[rs][cs]
        self.blow()

    def blow(self):
        k = 3
        for i in range(self.rows):
            for j in range(self.columns - 2):
                if len(set(self._pieces[i][j:j + k])) == 1:
                    self._pieces[i][j:j + k] = [Empty(self.piece_size)] * k
        for i in range(self.rows - 2):
            for j in range(self.columns):
                temp = set()
                for n in range(k):
                    temp.add(self._pieces[i + n][j])
                if len(temp) == 1:
                    for n in range(k):
                        self._pieces[i + n][j] = Empty(self.piece_size)

    def draw(self, dest=(0, 0)):
        self.surface.fill(BACKGROUND_COLOR)

        for i in range(self.rows + 1):
            pygame.draw.line(
                self.surface, self.grid_color,
                (0, i * self.cell_size), (self.columns * self.cell_size, i * self.cell_size),
                self.grid_width
            )
        for i in range(self.columns + 1):
            pygame.draw.line(
                self.surface, self.grid_color,
                (i * self.cell_size, 0), (i * self.cell_size, self.rows * self.cell_size),
                self.grid_width
            )

        shift = (self.cell_size - self.piece_size) // 2
        for i in range(self.rows):
            y = i * self.cell_size + shift
            for j in range(self.columns):
                x = j * self.cell_size + shift
                self._pieces[i][j].draw(self.surface, (x, y))

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


def main():
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h))
    Field(screen).run()


if __name__ == '__main__':
    main()

pygame.quit()
