import curses
import os

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Create a new window for file explorer
    win1 = curses.newwin(20, 40, 0, 0)
    win1.addstr(0, 0, "File Explorer")
    win1.refresh()

    # Create another window for directory information
    win2 = curses.newwin(20, 40, 0, 40)
    win2.addstr(0, 0, "Directory Information")
    win2.refresh()

    # Get current working directory
    cwd = os.getcwd()

    # Display directory information in second window
    win2.addstr(2, 0, "Current Directory: " + cwd)
    win2.addstr(4, 0, "Contents:")
    for i, item in enumerate(os.listdir(cwd)):
        win2.addstr(5+i, 2, item)

    win2.refresh()

    # Navigation loop
    while True:
        # Get user input
        c = stdscr.getkey()

        # Check if user wants to quit
        if c == 'q':
            break

        # Check if user wants to go up a directory
        elif c == 'u':
            os.chdir('..')

        # Check if user wants to enter a directory
        elif c.isdigit():
            index = int(c)
            dir_name = os.listdir(cwd)[index]
            os.chdir(dir_name)

        # Update current working directory
        cwd = os.getcwd()

        # Clear second window
        win2.clear()
        win2.addstr(0, 0, "Directory Information")

        # Display updated directory information in second window
        win2.addstr(2, 0, "Current Directory: " + cwd)
        win2.addstr(4, 0, "Contents:")
        for i, item in enumerate(os.listdir(cwd)):
            win2.addstr(5+i, 2, item)

        win2.refresh()

curses.wrapper(main)