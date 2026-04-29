import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    h, w = stdscr.getmaxyx()

    # Initial snake
    snake = [(h // 2, w // 4 + i) for i in range(3)]
    direction = curses.KEY_RIGHT

    # Initial food
    food = (random.randint(1, h - 2), random.randint(1, w - 2))
    stdscr.addch(food[0], food[1], "o")

    score = 0

    while True:
        key = stdscr.getch()

        if key == ord("q"):
            break

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            opposite = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
                       curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT}
            if key != opposite.get(direction):
                direction = key

        head = snake[-1]
        if direction == curses.KEY_UP:
            new_head = (head[0] - 1, head[1])
        elif direction == curses.KEY_DOWN:
            new_head = (head[0] + 1, head[1])
        elif direction == curses.KEY_LEFT:
            new_head = (head[0], head[1] - 1)
        elif direction == curses.KEY_RIGHT:
            new_head = (head[0], head[1] + 1)

        # Check collision
        if (new_head[0] <= 0 or new_head[0] >= h - 1 or
            new_head[1] <= 0 or new_head[1] >= w - 1 or
            new_head in snake):
            break

        snake.append(new_head)

        if new_head == food:
            score += 1
            food = (random.randint(1, h - 2), random.randint(1, w - 2))
            stdscr.addch(food[0], food[1], "o")
        else:
            tail = snake.pop(0)
            stdscr.addch(tail[0], tail[1], " ")

        stdscr.addch(new_head[0], new_head[1], "@")
        stdscr.addstr(0, 2, f" Score: {score} ")

    stdscr.addstr(h // 2, w // 2 - 5, f"GAME OVER! Score: {score}")
    stdscr.nodelay(0)
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
