from picotui.context import Context
from picotui.screen import Screen
from picotui.widgets import WLabel, WButton

with Context():
    Screen.init_tty()
    Screen.cls()
    Screen.attr_color(Screen.C_WHITE, Screen.C_BLUE)
    Screen.puts(0, 0, "Hello World!")
    d = Dialog(5, 5, 50, 12)
    d.add(1, 1, WLabel("Name:"))
    d.add(11, 1, WTextEntry(16, "John Doe"))
    b = WButton(10, "OK")
    d.add(10, 4, b)
    b.finish_dialog = ACTION_OK
    res = d.loop()
Screen.goto(0, 20)
Screen.attr_reset()
Screen.cls()
Screen.goto(0, 0)
