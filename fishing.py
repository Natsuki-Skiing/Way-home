import curses
import time
import random

def fishing(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Create two windows: one for bar and one for messages
    bar_win = curses.newwin(3, 40, height // 2 - 1, (width - 40) // 2)
    msg_win = curses.newwin(5, 40, height // 2 + 3, (width - 40) // 2)

    def draw_bar(win, length, hit_range):
        position = 0
        direction = 1
        hit_start = random.randint(5, length - hit_range - 5)
        hit_end = hit_start + hit_range

        while True:
            win.clear()
            for i in range(length):
                if hit_start <= i < hit_end:
                    win.addch(1, i, ord('#'))
                else:
                    win.addch(1, i, ord('-'))
            win.addch(1, position, ord('*'))
            win.refresh()

            key = stdscr.getch()
            if key == ord(' '):
                return hit_start <= position < hit_end

            position += direction
            if position == 0 or position == length - 1:
                direction *= -1

            time.sleep(0.02)

    msg_win.addstr(0, 0, "Cast your line! Timing is key.")
    msg_win.addstr(1, 0, "Press SPACE when the * is in the '#' zone")
    msg_win.refresh()
    time.sleep(1.5)

    # Horizontal bar timing
    success = draw_bar(bar_win, 30, 6)
    if not success:
        msg_win.clear()
        msg_win.addstr(0, 0, "The fish got away! Try again.")
        msg_win.refresh()
        stdscr.getch()
        return

    msg_win.clear()
    msg_win.addstr(0, 0, "Nice catch on horizontal! Now vertical...")
    msg_win.refresh()
    time.sleep(1.5)

    # Vertical bar timing
    def draw_vertical_bar(win, height, hit_range):
        position = 0
        direction = 1
        hit_start = random.randint(2, height - hit_range - 2)
        hit_end = hit_start + hit_range

        while True:
            win.clear()
            for i in range(height):
                if hit_start <= i < hit_end:
                    win.addch(i, 2, ord('#'))
                else:
                    win.addch(i, 2, ord('|'))
            win.addch(position, 2, ord('*'))
            win.refresh()

            key = stdscr.getch()
            if key == ord(' '):
                return hit_start <= position < hit_end

            position += direction
            if position == 0 or position == height - 1:
                direction *= -1

            time.sleep(0.1)

    vert_win = curses.newwin(20, 5, height // 2 - 10, (width - 5) // 2)
    success = draw_vertical_bar(vert_win, 20, 4)

    msg_win.clear()
    if success:
        msg_win.addstr(0, 0, "You caught a fish! 🎣")
    else:
        msg_win.addstr(0, 0, "The fish slipped away on vertical!")
    msg_win.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(fishing)
 