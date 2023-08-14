import argparse
import curses
import pathlib

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border(0)

    def draw_grid(self, screen) -> None:
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                screen.addch(y + 1, x + 1, "*" if cell else " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.resize(self.life.rows + 2, self.life.cols + 2)

        running = True

        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()
            curses.napms(100)

        screen.getch()

        curses.endwin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск игры 'Жизнь' в консоли")

    parser.add_argument("--rows", type=int, default=24, help="Количество строк игрового поля")
    parser.add_argument("--cols", type=int, default=80, help="Количество столбцов игрового поля")
    parser.add_argument(
        "--max-generations", type=float, default=float("inf"), help="Максимальное число поколений"
    )
    parser.add_argument(
        "--file", type=pathlib.Path, help="Загрузить начальное состояние игры из файла"
    )

    args = parser.parse_args()

    if args.file:
        life = GameOfLife.from_file(args.file)
    else:
        rows = args.rows
        cols = args.cols
        max_generations = args.max_generations
        life = GameOfLife((rows, cols), max_generations=max_generations)

    ui = Console(life)
    ui.run()
