import curses
curses.is_enter = lambda key: key == curses.KEY_ENTER or key == 10 or key == 13
