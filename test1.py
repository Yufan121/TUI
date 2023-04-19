import os
from cursesmenu import *
from cursesmenu.items import *

def open_file(file):
    os.system('xdg-open ' + file)

menu = CursesMenu("File Browser", "Select a file to open")
for file in os.listdir(os.getcwd()):
    menu.append_item(FunctionItem(file, open_file, [file]))
menu.show()