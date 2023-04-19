"""
A TUI-based file browser 
Code structure: Class-based
"""


class FileBrowser:
    def __init__(self, directory):
        self.directory = directory
        self.current_selection = 0
        self.files = os.listdir(directory)

    def display(self):
        # Display the files in the directory
        for i, file in enumerate(self.files):
            if i == self.current_selection:
                print("> " + file)
            else:
                print("  " + file)

    def move_selection_up(self):
        # Move the selection up
        if self.current_selection > 0:
            self.current_selection -= 1

    def move_selection_down(self):
        # Move the selection down
        if self.current_selection < len(self.files) - 1:
            self.current_selection += 1

    def open_selected_file(self):
        # Open the selected file
        file = self.files[self.current_selection]
        os.system('xdg-open ' + os.path.join(self.directory, file))