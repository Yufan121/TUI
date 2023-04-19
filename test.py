import curses
import os
import time
import threading

# a TUI-based file browser

def get_dir_info(dir_path):
    num_files = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                num_files += 1
                total_size += os.path.getsize(file_path)
    return num_files, total_size



def file_browser(stdscr):
    current_dir = os.getcwd()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    cursor_pos = 0
    dir_info = {}

    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "Current directory: {}".format(current_dir))
        files = os.listdir(current_dir)
        files.insert(0, "..")
        
        for i, f in enumerate(files):
            file_path = os.path.join(current_dir, f)
            if os.path.isfile(file_path):
                file_info = os.stat(file_path)
                file_size = file_info.st_size
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_mtime))
                stdscr.addstr(i + 2, 0, "{} ".format(f))
                stdscr.addstr("({} bytes, last modified {})".format(file_size, file_mtime), curses.color_pair(1))
            elif os.path.isdir(file_path):
                if file_path in dir_info: # already calculated, just display
                    num_files, total_size = dir_info[file_path]
                    stdscr.addstr(i + 2, 0, "{} ".format(f))
                    stdscr.addstr("({} files, {} bytes)".format(num_files, total_size), curses.color_pair(1))
                else: # calculate in a separate thread
                    stdscr.addstr(i + 2, 0, "{} (calculating...)".format(f))
                    t = threading.Thread(target=get_dir_info, args=(file_path, dir_info))
                    t.start()
            else:
                stdscr.addstr(i + 2, 0, f)
            if i == cursor_pos:
                stdscr.addstr(i + 2, 0, f, curses.A_REVERSE)

        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_UP:
            cursor_pos -= 1 if cursor_pos > 0 else 0
        elif c == curses.KEY_DOWN:
            cursor_pos += 1 if cursor_pos < len(files) - 1 else 0
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            new_dir = os.path.join(current_dir, files[cursor_pos])
            if os.path.isdir(new_dir):
                current_dir = new_dir
                cursor_pos = 0 
            elif os.path.isfile(new_dir): # open file
                pass
                
curses.wrapper(file_browser)




import os
import time
import threading

def get_dir_info(dir_path, result):
    num_files = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                num_files += 1
                total_size += os.path.getsize(file_path)
    result[dir_path] = (num_files, total_size)

def file_browser(stdscr):
    current_dir = os.getcwd()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    cursor_pos = 0
    dir_info = {}
    
    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "Current directory: {}".format(current_dir))
        files = os.listdir(current_dir)
        files.insert(0, "..")
        
        for i, f in enumerate(files):
            file_path = os.path.join(current_dir, f)
            if os.path.isfile(file_path):
                file_info = os.stat(file_path)
                file_size = file_info.st_size
                file_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_mtime))
                stdscr.addstr(i + 2, 0, "{} ".format(f))
                stdscr.addstr("({} bytes, last modified {})".format(file_size, file_mtime), curses.color_pair(1))
            elif os.path.isdir(file_path):
                if file_path in dir_info:
                    num_files, total_size = dir_info[file_path]
                    stdscr.addstr(i + 2, 0, "{} ".format(f))
                    stdscr.addstr("({} files, {} bytes)".format(num_files, total_size), curses.color_pair(1))
                else:
                    stdscr.addstr(i + 2, 0, "{} (calculating...)".format(f))
                    t = threading.Thread(target=get_dir_info, args=(file_path, dir_info))
                    t.start()
            else:
                stdscr.addstr(i + 2, 0, f)
            if i == cursor_pos:
                stdscr.addstr(i + 2, 0, f, curses.A_REVERSE)

        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_UP:
            cursor_pos -= 1 if cursor_pos > 0 else 0
        elif c == curses.KEY_DOWN:
            cursor_pos += 1 if cursor_pos < len(files) - 1 else 0
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            new_dir = os.path.join(current_dir, files[cursor_pos])
            if os.path.isdir(new_dir):
                current_dir = new_dir
                cursor_pos = 0 

curses.wrapper(file_browser)
