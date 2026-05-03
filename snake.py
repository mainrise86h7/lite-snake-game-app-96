import curses
import random

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.h, self.w = stdscr.getmaxyx()
        self.score = 0
        self.speed = 100
        self.snake = [(self.h // 2, self.w // 4 + i) for i in range(3)]
        self.direction = curses.KEY_RIGHT
        self.food = self._place_food()
        self.game_over = False

    def _place_food(self):
        while True:
            pos = (random.randint(1, self.h - 2), random.randint(1, self.w - 2))
            if pos not in self.snake:
                return pos

    def handle_input(self):
        key = self.stdscr.getch()
        if key == ord("q"):
            self.game_over = True
            return
        opposite = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT,
        }
        if key in opposite and key != opposite.get(self.direction):
            self.direction = key

    def update(self):
        head = self.snake[-1]
        moves = {
            curses.KEY_UP: (-1, 0),
            curses.KEY_DOWN: (1, 0),
            curses.KEY_LEFT: (0, -1),
            curses.KEY_RIGHT: (0, 1),
        }
        dy, dx = moves[self.direction]
        new_head = (head[0] + dy, head[1] + dx)

        # Wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.h - 1 or
            new_head[1] <= 0 or new_head[1] >= self.w - 1):
            self.game_over = True
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
            # Speed up slightly
            self.speed = max(50, self.speed - 2)
            self.stdscr.timeout(self.speed)
        else:
            tail = self.snake.pop(0)
            self.stdscr.addch(tail[0], tail[1], " ")

    def draw(self):
        if self.game_over:
            return
        head = self.snake[-1]
        self.stdscr.addch(head[0], head[1], "@")
        self.stdscr.addch(self.food[0], self.food[1], "o")
        self.stdscr.addstr(0, 2, f" Score: {self.score} | Speed: {100 - self.speed + 50} ")

    def show_game_over(self):
        msg = f"GAME OVER! Score: {self.score}"
        self.stdscr.addstr(self.h // 2, self.w // 2 - len(msg) // 2, msg)
        self.stdscr.addstr(self.h // 2 + 1, self.w // 2 - 10, "Press any key to exit")
        self.stdscr.nodelay(0)
        self.stdscr.getch()

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(self.speed)

        # Draw initial food
        self.stdscr.addch(self.food[0], self.food[1], "o")

        while not self.game_over:
            self.handle_input()
            if not self.game_over:
                self.update()
            if not self.game_over:
                self.draw()

        self.show_game_over()


def main(stdscr):
    game = SnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)
