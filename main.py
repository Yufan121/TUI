import curses
import os
import time
import threading
import subprocess

import slurm
import fileManager

'''
A TUI-based file browser
- Displays the current directory
- Entering parent and child directories
- Displaying file information in a different color
- Calculating directory sizes in a separate thread, killing the thread when the user enters a new directory

'''



def get_dir_info(dir_path, result, stop_event, threads):
    num_files = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for f in filenames:
            if stop_event.is_set():
                return
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                num_files += 1
                total_size += os.path.getsize(file_path)
    
    result[dir_path] = (num_files, total_size)
    # remove itself from the thread manager
    del threads[dir_path]

def get_color(size): # returns the color pair number
    if size < 1024:
        return 1
    elif size < 1024 * 1024:
        return 2
    elif size < 1024 * 1024 * 1024:
        return 3
    else:
        return 4

def format_size(size):
    if size < 1024:
        return "{} bytes".format(size)
    elif size < 1024 * 1024:
        return "{:.2f} KB".format(size / 1024)
    elif size < 1024 * 1024 * 1024:
        return "{:.2f} MB".format(size / (1024 * 1024))
    else:
        return "{:.2f} GB".format(size / (1024 * 1024 * 1024))

def get_slurm_jobs(current_dir): # get slurm jobs with working directory same as current directory
    jobs = []
    p = subprocess.Popen(["squeue", "--me", '-o%.7i %.11b %.16R %.30j %.2t %.10M %.6D %.3C %.8Q %Z'], stdout=subprocess.PIPE)
    for line in p.stdout:
        line = line.decode("utf-8")
        if current_dir in line:
            jobs.append(line)
    return jobs


def file_browser(stdscr):
    current_dir = os.getcwd()
    curses.curs_set(0)
    # stdscr.nodelay(1)
    # stdscr.halfdelay()
    stdscr.timeout(100)

    cursor_pos = 0
    dir_info = {} # stores the directory sizes, no locks present so be careful
    threads = {}
    stop_event = threading.Event()

    
    # get custom color pairs of 4 different levels of green 
    curses.init_color(1, 800, 800, 800)
    curses.init_color(2, 400, 800, 400)
    curses.init_color(3, 200, 800, 200)
    curses.init_color(4, 0, 800, 0)

    # Initialize color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    
    while True:
        # update slurm.current_dir
        slurm.current_dir = current_dir
        
        # erase the screen 
        stdscr.erase()
        
        # Display the current directory
        stdscr.addstr(0, 0, "Current directory: {}".format(current_dir))
        
        # Display the files in the current directory
        files = os.listdir(current_dir)
        files.insert(0, "..")
        files.sort()
        # get screen width and height in unit of characters
        screen_height, screen_width = stdscr.getmaxyx()
        # curses.mousemask(curses.ALL_MOUSE_EVENTS)

        # Display the files
        for i, f in enumerate(files):
            file_path = os.path.join(current_dir, f)
            if i + 2 < screen_height and files[i] != "..":
                if os.path.isfile(file_path):
                    file_info = os.stat(file_path)
                    file_size = file_info.st_size
                    file_mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_mtime))
                    stdscr.addstr(i + 2, 0, "{} ".format(f)) 
                    
                    # Display file size and last modified time
                    info_str = "({}, last modified {})".format(format_size(file_size), file_mtime)
                    stdscr.addstr(i + 2, screen_width - 2 - len(info_str), info_str, curses.color_pair(get_color(file_size)))
                elif os.path.isdir(file_path):
                    if file_path in dir_info and dir_info[file_path] == '': # calculating
                        stdscr.addstr(i + 2, 0, "{} ".format(f))
                        stdscr.addstr(i + 2, screen_width - 2 - 10, "calculating...")
                    elif file_path in dir_info: # already calculated, just display
                        num_files, total_size = dir_info[file_path]
                        stdscr.addstr(i + 2, 0, "{} ".format(f))
                        
                        # Display number of files and total size
                        info_str = "({} files, {})".format(num_files, format_size(total_size))
                        stdscr.addstr(i + 2, screen_width - 2 - len(info_str), info_str, curses.color_pair(get_color(total_size)))                        
                    else: # calculate in a separate thread
                        stdscr.addstr(i + 2, 0, "{} ".format(f))
                        # start the thread if total number of threads is less than 10
                        if len(threads) < 10:
                            dir_info[file_path]='' # we have file_path as unique identifier, so no more in the dict value
                            t = threading.Thread(target=get_dir_info, args=(file_path,  dir_info, stop_event, threads))
                            threads[file_path] = t
                            t.start()
                        else: # if there are already 10 threads, display "pending"
                            stdscr.addstr(i + 2, screen_width - 2 - 10, "pending...")

                else:
                    stdscr.addstr(i + 2, 0, f)
                if i == cursor_pos:
                    stdscr.addstr(i + 2, 0, f, curses.A_REVERSE)


        
        # get slurm jobs by directory
        jobs = slurm.jobs_in_current_dir
    
        # Display slurm jobs
        stdscr.addstr(screen_height - 11, 0, "Slurm jobs:")
        for i, job in enumerate(jobs):
            stdscr.addstr(screen_height - 10 + i, 0, job) if i < 8 else stdscr.addstr(screen_height - 2, 0, "...")
            
                        
        # Catch user input 
        c = stdscr.getch() # 
        # quit, up, down, enter
        if c == ord('q'): # quit
            break
        if c == curses.KEY_UP: # up arrow
            cursor_pos -= 1 if cursor_pos > 0 else 0
        elif c == curses.KEY_DOWN: # down arrow
            cursor_pos += 1 if cursor_pos < len(files) - 1 else 0
            
        elif c == curses.KEY_ENTER or c == 10 or c == 13: # enter key
            new_dir = os.path.join(current_dir, files[cursor_pos])
            if os.path.isdir(new_dir):
                # Set the stop event and wait for all threads to finish
                stop_event.set() # set the stop event
                for t in threads.values():
                    t.join()
                # Reset the stop event and clear the threads and dir_info lists
                stop_event.clear()
                threads.clear()
                dir_info.clear()
                
                # Change the current directory
                current_dir = new_dir
                cursor_pos = 0 # reset cursor position
            elif os.path.isfile(new_dir): # open file
                # submit slurm job after user confirmation
                stdscr.addstr(screen_height - 1, 0, "Submit job for {}? (y/n)".format(new_dir))
                
                # wait for user to press y or n
                while c != ord('y') and c != ord('n'):
                    c = stdscr.getch()
                    if c == ord('y'):
                        # submit job
                        if slurm_installed:
                            subprocess.call(['sbatch', new_dir])
                        if figlet_installed:
                            # Run command and capture output
                            output = subprocess.check_output(['figlet', 'SUBMITTED']).decode('utf-8')
                            stdscr.addstr(screen_height // 2, 0, output)
                        if slurm_installed:
                            slurm.submit_job( new_dir )
                        else: # promt user to install slurm
                            stdscr.addstr(screen_height - 1, 0, "Please install slurm to submit jobs") # TODO: not showing up for whatever reason
                        stdscr.addstr(screen_height - 1, 0, "Submitted job for {}".format(new_dir))
                        stdscr.refresh()
                        time.sleep(2)
                        break
                    elif c == ord('n'):
                        # don't submit job, print message in big text and wait for 1 second
                        if figlet_installed:
                            output = subprocess.check_output(['figlet', 'NOT SUBMITTED']).decode('utf-8')
                            stdscr.addstr(screen_height // 2, 0, output)
                        stdscr.addstr(screen_height - 1, 0, "Okay, not submitting job for {}".format(new_dir))
                        # stdscr.addstr(screen_height - 1, 0, "Okay, not submitting job for {}".format(new_dir))
                        stdscr.refresh()
                        time.sleep(2)
                        break
                # clear screen
                stdscr.clear()


if __name__ == "__main__":

    
    figlet_installed = False
    try:
        subprocess.check_output(['which', 'figlet'])
        print('figlet is installed')
        figlet_installed = True
    except subprocess.CalledProcessError:
        print('figlet is not installed')
        figlet_installed = False

    # check if slurm is installed
    slurm_installed = False
    try:
        subprocess.check_output(['which', 'sbatch'])
        print('slurm is installed') 
        slurm_installed = True
    except subprocess.CalledProcessError:
        print('slurm is not installed')
        slurm_installed = False
        
        
    # thread list
    threads = []
    stop_event = threading.Event()
    
    # Initialize fileManager
    fman = fileManager.FileManager()
    
    
    # Initialize slurm
    slurm = slurm.Slurm()
    if slurm_installed:
        threads.append(threading.Thread(target=slurm.update_jobs_periodically, args=(None, None, stop_event)))
        threads.append(threading.Thread(target=slurm.update_jobs_by_dir_periodically, args=(None, None, stop_event)))

    # start all threads
    for t in threads:
        t.start()
    #
        
    
    # start curses 
    curses.wrapper(file_browser)

    
    # set stop event
    stop_event.set()
    
    # terminate all threads
    for t in threads:
        t.join()