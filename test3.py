import curses
import os

"""
This is a simple file browser written in Python using the curses library.
Mouse support is enabled, so you can use the mouse to select files.
"""

def open_file(file):
    os.system('xdg-open ' + file)

def file_browser(stdscr):
    # Initialize curses
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_selection = 0
    files = os.listdir(os.getcwd())

    # Enable mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    while True:
        # Clear the screen
        stdscr.clear()

        # Display the files
        for i, file in enumerate(files):
            if i == current_selection:
                stdscr.addstr(i, 0, file, curses.color_pair(1))
            else:
                stdscr.addstr(i, 0, file)

        # Get user input
        key = stdscr.getch()

        # Handle user input
        if key == curses.KEY_UP:
            if current_selection > 0:
                current_selection -= 1
        elif key == curses.KEY_DOWN:
            if current_selection < len(files) - 1:
                current_selection += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            open_file(files[current_selection])
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            if y < len(files):
                current_selection = y

# Run the file browser
curses.wrapper(file_browser)
