# import os
# import urwid

# def on_select(button, path):
#     if os.path.isdir(path):
#         show_dir(path)
#     else:
#         urwid.ExitMainLoop()

# def show_dir(path):
#     items = [urwid.Button(f, on_press=on_select, user_data=os.path.join(path, f)) for f in os.listdir(path)]
#     listbox = urwid.ListBox(urwid.SimpleFocusListWalker(items))
#     loop.widget = urwid.Filler(listbox)

# loop = urwid.MainLoop(urwid.Filler(urwid.Text('')))
# show_dir(os.getcwd())
# loop.run()

import urwid

def save(key):
    if key == 'ctrl s':
        with open('file.txt', 'w') as f:
            f.write(edit.get_edit_text())
        view.set_footer(urwid.AttrMap(urwid.Text('Saved'), 'success'))

palette = [
    ('success', 'black', 'light green'),
]

edit = urwid.Edit(multiline=True)
view = urwid.Frame(edit, footer=urwid.AttrMap(urwid.Text('Ctrl+S to save'), 'success'))
loop = urwid.MainLoop(view, palette, unhandled_input=save)
loop.run()