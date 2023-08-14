import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell

        row_start, row_end = max(0, row - 1), min(self.rows, row + 2)
        col_start, col_end = max(0, col - 1), min(self.cols, col + 2)

        return [
            self.curr_generation[i][j]
            for i in range(row_start, row_end)
            for j in range(col_start, col_end)
            if (i, j) != (row, col)
        ]

    def get_next_generation(self) -> Grid:
        new_generation = self.create_grid()

        for i in range(self.rows):
            for j in range(self.cols):
                cell = (i, j)
                live_neighbours = sum(self.get_neighbours(cell))

                is_alive = self.curr_generation[i][j] == 1

                new_generation[i][j] = int(
                    2 <= live_neighbours <= 3  # stays alive
                    if is_alive
                    else live_neighbours == 3  # can revive
                )

        return new_generation

    def step(self) -> None:
        if not self.is_max_generations_exceeded:
            if self.is_changing:
                self.prev_generation = self.curr_generation
                self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            return False

        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with filename.open() as fin:
            grid = [list(map(int, line.strip())) for line in fin if not line.isspace()]

        rows, cols = len(grid), len(grid[0])
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        with filename.open("w") as fout:
            for row in self.curr_generation:
                fout.write("".join(map(str, row)) + "\n")
