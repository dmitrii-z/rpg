import os, msvcrt, re, copy

class Window:
    def __init__(self, x, y, w, h, fill=' '):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._parent = None
        self.clear(fill)
        self._children = []

    def show(self):
        for i in range(self._h):
            print('\033[{};{}H{}'.format(self._y + i + 1, self._x + 1, ''.join(self._buffer[i])))
        for c in self._children:
            c.show()

    def clear(self, fill=' '):
        self._fill = fill
        self._buffer = []
        for i in range(self._h):
            self._buffer.append([self._fill] * self._w)

    def print_at(self, x, y, s, flush=False, align_right=False):
        if align_right:
            x = x - len(s) + 1
        if y < 0 or y >= self._h:
            return
        for i in range(min(len(s), self._w - x)):
            self._buffer[y][x + i] = s[i]
        if flush:
            print('\033[{};{}H{}'.format(self._y + y + 1, self._x + x + 1, s[:min(len(s), self._w - x)]), end='', flush=True)

    def create_child(self, x, y, w, h, fill=''):
        c = Window(self._x + x, self._y + y, min(w, self._w - x), min(h, self._h - y), fill if fill else self._fill)
        c._parent = self
        self._children.append(c)
        return c

    def remove_shild(self, child):
        self._children.remove(child)

    def child_at(self, z):
        return self._children[z] if z >= 0 and z < len(self._children) else None
    
    def release(self):
        if self._parent:
            self._parent.remove_shild(self)
            self._parent.show()
            self._parent = None
    
    def width(self):
        return self._w
    
    def height(self):
        return self._h
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.release()


def add_border(window: Window, x, y, w, h, bold=False):
    hdr = ('#' + '=' * (w - 2) + '#') if bold else ('+' + '-' * (w - 2) + '+')
    window.print_at(x, y, hdr)
    for i in range(h - 2):
        window.print_at(x, y + i + 1, '#' if bold else '|')
        window.print_at(x + w - 1, y + i + 1, '#' if bold else '|')
    window.print_at(x, y + h - 1, hdr)


def add_window_border(window: Window, bold=False):
    add_border(window, 0, 0, window.width(), window.height(), bold)


def add_v_line(window: Window, x, y=0, h=-1, bold=False):
    for i in range(y, y + h if h >= 0 else window.height()):
        window.print_at(x, i, '#' if bold else '|')


def max_width(lines):
    return len(max(lines, key=lambda x: len(x)))


class ArrowMenu:
    def __init__(self, window: Window, x, y, items, title='', current=0, min_w=0):
        self._title = title
        self._items = items
        self._current_item = current
        self._window = window.create_child(x, y, max(max(max_width(self._items), len(title)) + 3, min_w), len(self._items) + self._ybase())
        self._show()

    def _ybase(self):
        return 2 if self._title else 0

    def _show(self):
        if self._title:
            self._window.print_at(1, 0, self._title)
        for i, it in enumerate(self._items):
            self._window.print_at(2, i + self._ybase(), it)
        self._window.show()
        self._window.print_at(0, self._current_item + self._ybase(), '>', flush=True)

    def select(self):
        while True:
            key = ord(msvcrt.getwch())
            if key == 80 or key == 72:
                self._window.print_at(0, self._current_item + self._ybase(), ' ',  flush=True)
                while (True):
                    self._current_item = (self._current_item + (1 if key == 80 else -1)) % len(self._items)
                    if (self._items[self._current_item] != ''):
                        break
                self._window.print_at(0, self._current_item + self._ybase(), '>', flush=True)
            elif key == 77 or key == 13 or key == 75 or key == 27:
                return self._current_item, key != 75 and key != 27
            
    def set_item(self, index, item):
        self._window.print_at(2, index + self._ybase(), ' ' * len(self._items[index]), True)
        self._items[index] = item
        self._window.print_at(2, index + self._ybase(), item, True)
        self._window.print_at(0, self._current_item + self._ybase(), '>', True)

    def set_title(self, title):
        self._title = title
        self._show()

            
    def release(self):
        self._window.release()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.release()


class ArrowMenuDecorated:
    def __init__(self, window: Window, x, y, items, title='', current=0, bold=False):
        self._window = window.create_child(x, y, max(max_width(items), len(title)) + 5, len(items) + (2 if title else 0) + 2)
        add_window_border(self._window, bold)
        self._window.show()
        self._menu = ArrowMenu(self._window, 1, 1, items, title, current)

    def select(self):
        return self._menu.select()
    
    def set_item(self, index, item):
        self._menu.set_item(index, item)

    def set_title(self, title):
        self._menu.set_title(title)

    def release(self):
        self._window.release()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.release()


def get_input_name(window: Window, x, y, w, prompt, text='', allowed_symbols='a-zA-Z0-9'):
    with window.create_child(x, y, w, 1, ' ') as wnd:
        wnd.show()
        wnd.print_at(0, 0, prompt+text, flush=True)
        result = list(text)
        while True:
            ch = msvcrt.getwch()
            key = ord(ch)
            if key == 13:
                return ''.join(result)
            elif key == 27:
                return ''
            elif key == 8:
                if not result:
                    continue
                result = result[:-1]
                wnd.print_at(len(prompt) + len(result), 0, ' ', flush=True)
                wnd.print_at(len(prompt) + len(result), 0, '', flush=True)
            else:
                if not re.search('^[{}]$'.format(allowed_symbols), ch):
                    continue
                if len(prompt) + len(result) >= wnd.width():
                    continue
                wnd.print_at(len(prompt) + len(result), 0, ch, flush=True)
                result += ch


def get_input_name_decorated(window: Window, x, y, w, prompt, text='', allowed_symbols='a-zA-Z0-9', bold=False):
    with window.create_child(x, y, w, 3) as wnd:
        add_window_border(wnd, bold)
        wnd.show()
        return get_input_name(wnd, 2, 1, w - 4, prompt, text, allowed_symbols)


def get_open_file_name(window: Window, x, y, title, dir, ext):
    try:
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(ext)]
    except:
        return None
    options = [f[:-len(ext)] for f in files] + ['', 'Cancel']
    with window.create_child(x, y, max(max_width(options), len(title)) + 6, len(options) + 4) as wnd:
        add_window_border(wnd)
        wnd.show()
        with ArrowMenu(wnd, 2, 1, options, title) as menu:
            while(True):
                id, fwd = menu.select()
                if not fwd:
                    return None
                if id < len(files):
                    return files[id]
                elif id == len(files) + 1:
                    return None


MainWindowWidth = 80
MainWindowHeight = 25
MainWindowBackground = '.'
MainWindow = Window(0, 0, MainWindowWidth, MainWindowHeight)

def mw():
    return MainWindow

def clean_on_exit():
    print('\033[{};{}H'.format(MainWindowHeight - 1, 0))


def navigate_controller(exit_callback, enter_callback, num_indexes_h, num_indexes_v=0, index_h=0, index_v=0):
    enter_callback(index_h, index_v)
    while True:
        key = ord(msvcrt.getwch())
        if key == 13:
            exit_callback(index_h, index_v)
            return index_h, index_v
        elif key == 27:
            exit_callback(index_h, index_v)
            return None, None
        elif key == 77 or key == 75: # >80 <72
            exit_callback(index_h, index_v)
            index_h = (index_h + (1 if key == 77 else -1)) % num_indexes_h
            enter_callback(index_h, index_v)
        elif key == 80 or key == 72:
            exit_callback(index_h, index_v)
            index_v = (index_v + (1 if key == 80 else -1)) % num_indexes_v
            enter_callback(index_h, index_v)


class TextArea:
    def __init__(self, window: Window, x, y, w, h, auto_scroll_down=True):
        self._lines = []
        self._wnd = window.create_child(x, y, w, h)
        self._textw = w - 1
        self._texth = h
        self._top_line = 0
        self._auto_scroll_down = auto_scroll_down

    def _update(self):
        for i in range(self._texth):
            l = self._lines[self._top_line + i] if len(self._lines) > self._top_line + i else ''
            self._wnd.print_at(0, i, '{}{}'.format(l, ' ' * (self._textw - len(l) + 1)))
        if self._top_line > 0:
            positions = len(self._lines) - self._texth + 1 if len(self._lines) > self._texth else 1
            ratio = float(self._top_line + 1) / positions
            pos = int(ratio * self._texth) - 1
            self._wnd.print_at(self._textw, pos, 'O')

    def show(self):
        self._update()
        self._wnd.show()
    
    def clear(self):
        self._lines = []
        self._top_line = 0
        self.show()

    def add(self, line, flush=True):
        self._lines += [line[i * self._textw:(i + 1) * self._textw] for i in range(int(len(line) / self._textw) + (1 if len(line) % self._textw > 0 else 0))]
        if self._auto_scroll_down:
            self._top_line = max(0, len(self._lines) - self._texth)
        self._update()
        if flush:
            self._wnd.show()


def splash_decorated(window: Window, x, y, w, text: str, bold=False):
    textw = w - 4
    lines = [text[i * textw:(i + 1) * textw] for i in range(int(len(text) / textw) + (1 if len(text) % textw > 0 else 0))]
    h = 2 + len(lines)
    wnd = window.create_child(x, y, w, h)
    add_window_border(wnd, bold)
    for i in range(len(lines)):
        wnd.print_at(2, i + 1, lines[i])
    wnd.show()
    msvcrt.getwch()
    wnd.release()