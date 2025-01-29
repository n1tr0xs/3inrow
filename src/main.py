import random
import pygame

DISPLAY_SIZE = (1280, 720)

pygame.init()


class Field:
    _background_color = (0, 0, 0)
    _grid_color = (255, 255, 255)
    _shrink = .8

    def __init__(self, rows: int = 5, columns: int = 5):
        self.cell_size = 60
        self.piece_size = self.cell_size * self._shrink
        self.rows = rows
        self.columns = columns

        self.screen = None
        self._clock = pygame.time.Clock()
        self.generate_pieces()  # self._pieces

    def generate_pieces(self):
        pieces = [
            Circle(self._background_color, self.piece_size, self.piece_size),
            Square(self._background_color, self.piece_size, self.piece_size),
            Triangle(self._background_color, self.piece_size, self.piece_size),
        ]

        self._pieces = [[None] * self.rows for i in range(self.columns)]

        for row in range(self.rows):
            for col in range(self.columns):
                random.shuffle(pieces)
                for piece in pieces:
                    if self.is_valid(row, col, piece):
                        self._pieces[row][col] = piece
                        break
        return self._pieces

    def is_valid(self, row: int, col: int, piece: 'Piece'):
        if col >= 2 and self._pieces[row][col - 1] == piece and self._pieces[row][col - 2] == piece:
            return False

        if row >= 2 and self._pieces[row - 1][col] == piece and self._pieces[row - 2][col] == piece:
            return False
        return True

    def run(self):
        width = self.rows * self.cell_size
        height = self.columns * self.cell_size
        self.screen = pygame.display.set_mode((width, height))
        running = True
        while running:
            while (event := pygame.event.poll()):
                if event.type == pygame.QUIT:
                    return

            self.draw()
            self._clock.tick(60)

    def draw(self):
        if not self.screen:
            return

        self.screen.fill(self._background_color)
        self.draw_grid()

        shift = (self.cell_size - self.piece_size) // 2
        for i in range(self.rows):
            y = i * self.cell_size + shift
            for j in range(self.columns):
                x = j * self.cell_size + shift
                self._pieces[i][j].draw(self.screen, (x, y))

        pygame.display.flip()

    def draw_grid(self):
        if not self.screen:
            return
        # вертикальные линии
        for i in range(1, self.rows):
            pygame.draw.line(
                self.screen, self._grid_color,
                (self.cell_size * i, 0), (self.cell_size * i, self.cell_size * self.columns)
            )
        # горизонтальные линии
        for i in range(1, self.columns):
            pygame.draw.line(
                self.screen, self._grid_color,
                (0, self.cell_size * i), (self.cell_size * self.rows, self.cell_size * i)
            )


class Piece:
    def __init__(self, bg_color, width: int, height: int):
        self.image = pygame.surface.Surface([width, height])
        self.image.fill(bg_color)

        self.rect = self.image.get_rect()

    def draw(self, surface, center: tuple[int, int]):
        surface.blit(self.image, center)

    def __eq__(self, other: 'Piece'):
        return isinstance(self, type(other))


class Circle(Piece):
    _color = 'green'

    def __init__(self, bg_color, width: int, height: int):
        super().__init__(bg_color, width, height)

        pygame.draw.circle(
            self.image, self._color,
            (width // 2, height // 2), width // 2,
        )

    def __str__(self):
        return 'Circle'

    def __repr__(self):
        return 'Circle'


class Square(Piece):
    _color = 'blue'

    def __init__(self, bg_color, width: int, height: int):
        super().__init__(bg_color, width, height)

        pygame.draw.rect(
            self.image, self._color,
            (0, 0, width, height),
        )

    def __str__(self):
        return 'Square'

    def __repr__(self):
        return 'Square'


class Triangle(Piece):
    _color = 'red'

    def __init__(self, bg_color, width: int, height: int):
        super().__init__(bg_color, width, height)

        pygame.draw.polygon(
            self.image, self._color,
            ((0, height), (width // 2, 0), (width, height)),
        )

    def __str__(self):
        return 'Triangle'

    def __repr__(self):
        return 'Triangle'


def main():
    Field().run()


if __name__ == '__main__':
    main()

pygame.quit()
