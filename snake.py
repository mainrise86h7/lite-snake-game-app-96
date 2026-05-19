import curses
import random
import argparse
import sys

DIFFICULTIES = {
    "easy": 150,
    "medium": 100,
    "hard": 60,
    "insane": 30,
}

MIN_HEIGHT = 10
MIN_WIDTH = 20

class GameError(Exception):
    pass

class SnakeGame:
    def __init__(self, stdscr, speed=100, wrap=False):
        self.stdscr = stdscr
        self.h, self.w = stdscr.getmaxyx()
        if self.h < MIN_HEIGHT or self.w < MIN_WIDTH:
            raise GameError(f"Terminal too small: {self.w}x{self.h} (need {MIN_WIDTH}x{MIN_HEIGHT})")
        self.score = 0
        self.speed = speed
        self.wrap = wrap
        self.snake = [(self.h // 2, self.w // 4 + i) for i in range(3)]
        self.direction = curses.KEY_RIGHT
        self.food = self._place_food()
        self.game_over = False

    def _place_food(self):
        attempts = 0
        while attempts < 1000:
            pos = (random.randint(1, self.h - 2), random.randint(1, self.w - 2))
            if pos not in self.snake:
                return pos
            attempts += 1
        raise GameError("Cannot place food - snake fills the board!")

    def handle_input(self):
        try:
            key = self.stdscr.getch()
        except curses.error:
            return
        if key == ord("q"):
            self.game_over = True
            return
        if key == ord("p"):
            self._pause()
            return
        opposite = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT,
        }
        if key in opposite and key != opposite.get(self.direction):
            self.direction = key

    def _pause(self):
        self.stdscr.addstr(self.h // 2, self.w // 2 - 4, " PAUSED ")
        self.stdscr.nodelay(0)
        self.stdscr.getch()
        self.stdscr.nodelay(1)

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

        if self.wrap:
            new_head = (new_head[0] % (self.h - 1) or 1, new_head[1] % (self.w - 1) or 1)
        else:
            if (new_head[0] <= 0 or new_head[0] >= self.h - 1 or
                new_head[1] <= 0 or new_head[1] >= self.w - 1):
                self.game_over = True
                return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
            self.speed = max(30, self.speed - 2)
            self.stdscr.timeout(self.speed)
        else:
            tail = self.snake.pop(0)
            try:
                self.stdscr.addch(tail[0], tail[1], " ")
            except curses.error:
                pass

    def draw(self):
        if self.game_over:
            return
        head = self.snake[-1]
        try:
            self.stdscr.addch(head[0], head[1], "@")
            self.stdscr.addch(self.food[0], self.food[1], "o")
            self.stdscr.addstr(0, 2, f" Score: {self.score} | Len: {len(self.snake)} ")
        except curses.error:
            pass

    def show_game_over(self):
        msg = f"GAME OVER! Score: {self.score}"
        try:
            self.stdscr.addstr(self.h // 2, self.w // 2 - len(msg) // 2, msg)
            self.stdscr.addstr(self.h // 2 + 1, self.w // 2 - 10, "Press any key to exit")
        except curses.error:
            pass
        self.stdscr.nodelay(0)
        self.stdscr.getch()

    def run(self):
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(self.speed)
        try:
            self.stdscr.addch(self.food[0], self.food[1], "o")
        except curses.error:
            pass

        while not self.game_over:
            self.handle_input()
            if not self.game_over:
                self.update()
            if not self.game_over:
                self.draw()

        self.show_game_over()
        return self.score


def parse_args():
    parser = argparse.ArgumentParser(description="Snake Game")
    parser.add_argument("-d", "--difficulty", choices=DIFFICULTIES.keys(), default="medium")
    parser.add_argument("--wrap", action="store_true", help="Wrap around edges")
    return parser.parse_args()


def main(stdscr):
    args = parse_args()
    speed = DIFFICULTIES[args.difficulty]
    try:
        game = SnakeGame(stdscr, speed=speed, wrap=args.wrap)
        final_score = game.run()
    except GameError as e:
        stdscr.addstr(0, 0, f"Error: {e}")
        stdscr.nodelay(0)
        stdscr.getch()
        return

    # Ask for name for high score
    from scores import save_score
    stdscr.addstr(stdscr.getmaxyx()[0] // 2 + 3, stdscr.getmaxyx()[1] // 2 - 12, "Enter name for scoreboard: ")
    curses.echo()
    name = stdscr.getstr().decode("utf-8").strip()
    if name:
        rank = save_score(name, final_score, args.difficulty)


if __name__ == "__main__":
    curses.wrapper(main)
