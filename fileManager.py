"""
fileManager.py
"""

import os
import threading
import time

class FileManager:
    """
    FileManager
    """

    

    def __init__(self):
        self.current_dir = ""
        self.dir_list = [] # list of contents in the current directory
        
    def get_dir_info(dir_path, result, stop_event):
        """
        get the number of files and total size of a directory
        """
        
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

    def format_size(size):
        """
        format the size of a file to GB, MB, KB, or bytes
        """
        if size < 1024:
            return "{} bytes".format(size)
        elif size < 1024 * 1024:
            return "{:.2f} KB".format(size / 1024)
        elif size < 1024 * 1024 * 1024:
            return "{:.2f} MB".format(size / (1024 * 1024))
        else:
            return "{:.2f} GB".format(size / (1024 * 1024 * 1024))

    def update_dir_list(self, current_dir):
        """
        update the list of contents in the current directory
        """
        self.dir_list = os.listdir(current_dir)
        self.dir_list.sort()
        self.dir_list.insert(0, "..")

    def update_dir_info(self, current_dir):
        """
        update the number of files and total size of a directory
        """
        dir_info = {}
        threads = []
        stop_event = threading.Event()
        for dirpath, dirnames, filenames in os.walk(current_dir):
            if dirpath not in dir_info:
                t = threading.Thread(target=self.get_dir_info, args=(dirpath, dir_info, stop_event))
                t.start()
                threads.append(t)
        for t in threads:
            t.join()
        return dir_info
    
    def update_dir_list_periodically(self, current_dir):
        """
        update the list of contents in the current directory periodically
        """
        while True:
            self.update_dir_list(current_dir)
            time.sleep(1)
