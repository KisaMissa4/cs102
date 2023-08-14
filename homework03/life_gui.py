import argparse

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        width: int = 640,
        height: int = 480,
        cell_size: int = 10,
        speed: int = 10,
    ) -> None:
        super().__init__(life)

        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed

        self.screen_size = width, height

        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = (
                    pygame.Color("green")
                    if self.life.curr_generation[row][col]
                    else pygame.Color("white")
                )
                rect = pygame.Rect(
                    col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        pygame.init()

        paused = True  # Игра начинается на паузе
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                # Нажатие пробела переключает паузу
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                # Обработка клика мыши для изменения состояния клетки
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // self.cell_size
                    row = y // self.cell_size
                    self.life.curr_generation[row][col] = not self.life.curr_generation[row][col]

            # Если игра не на паузе, обновляем состояние
            if not paused:
                self.life.step()

            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск игры 'Жизнь' в графическом интерфейсе")

    parser.add_argument("--width", type=int, default=640, help="Ширина игрового поля в пикселях")
    parser.add_argument("--height", type=int, default=480, help="Высота игрового поля в пикселях")
    parser.add_argument(
        "--cell-size", type=int, default=10, help="Размер клетки на игровом поле в пикселях"
    )
    parser.add_argument("--speed", type=int, default=10, help="Скорость")

    args = parser.parse_args()

    width = args.width
    height = args.height
    cell_size = args.cell_size
    speed = args.speed

    rows = height // cell_size
    cols = width // cell_size

    life = GameOfLife((rows, cols), randomize=False)

    ui = GUI(life, width, height, cell_size, speed)
    ui.run()
