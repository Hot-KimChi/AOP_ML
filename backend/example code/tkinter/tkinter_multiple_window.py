import tkinter as tk
import tkinter as ttk
import tkinter as tkfont


class Treeview(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.root = parent.winfo_toplevel()
        self.selected_items = []
        self.origin_x = \
            self.origin_y = \
            self.active_item = \
            self.origin_item = None

        sw = self.select_window = tk.Toplevel(self.root)
        sw.wait_visibility(self.root)
        sw.withdraw()
        sw.config(bg='#00aaff')
        sw.overrideredirect(True)
        sw.wm_attributes('-alpha', 0.3)
        sw.wm_attributes("-topmost", True)

        self.font = tkfont.nametofont('TkTextFont')
        self.style = parent.style
        self.linespace = self.font.metrics('linespace') + 5

        self.bind('<Escape>', self.tags_reset)
        self.bind('<Button-1>', self.button_press)
        self.bind('<ButtonRelease-1>', self.button_release)

    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]

    def tag_add(self, tags, item):
        self.tags_update('add', tags, item)

    def tag_remove(self, tags, item=None):
        self.tags_update('remove', tags, item)

    def tag_replace(self, old, new, item=None):
        for item in (item,) if item else self.tag_has(old):
            self.tags_update('add', new, item)
            self.tags_update('remove', old, item)

    def tags_reset(self, _=None):
        self.tag_remove(('selected', '_selected'))
        self.tag_replace('selected_odd', 'odd')
        self.tag_replace('selected_even', 'even')

    def tags_update(self, opt, tags, item):
        def get_items(node):
            items.append(node)
            for node in self.get_children(node):
                get_items(node)

        if not tags:
            return
        elif isinstance(tags, str):
            tags = (tags,)

        if not item:
            items = []
            for child in self.get_children():
                get_items(child)
        else:
            items = (item,)

        for item in items:
            _tags = list(self.item(item, 'tags'))
            for _tag in tags:
                if opt == 'add':
                    if _tag not in _tags:
                        _tags.append(_tag)
                elif opt == 'remove':
                    if _tag in _tags:
                        _tags.pop(_tags.index(_tag))
            self.item(item, tags=_tags)

    def button_press(self, event):
        self.origin_x, self.origin_y = event.x, event.y
        item = self.origin_item = self.active_item = self.identify('item', event.x, event.y)

        sw = self.select_window
        sw.geometry('0x0+0+0')
        sw.deiconify()

        self.bind('<Motion>', self.set_selected)

        if not item:
            if not event.state & 1 << 2:
                self.tags_reset()
            return

        if event.state & 1 << 2:
            if self.tag_has('odd', item):
                self.tag_add('selected', item)
                self.tag_replace('odd', 'selected_odd', item)
            elif self.tag_has('even', item):
                self.tag_add('selected', item)
                self.tag_replace('even', 'selected_even', item)
            elif self.tag_has('selected_odd', item):
                self.tag_replace('selected_odd', 'odd', item)
            elif self.tag_has('selected_even', item):
                self.tag_replace('selected_even', 'even', item)
        else:
            self.tags_reset()
            self.tag_add('selected', item)
            if self.tag_has('odd', item):
                self.tag_replace('odd', 'selected_odd', item)
            elif self.tag_has('even', item):
                self.tag_replace('even', 'selected_even', item)

    def button_release(self, _):
        self.select_window.withdraw()
        self.unbind('<Motion>')

        for item in self.selected_items:
            if self.tag_has('odd', item) or self.tag_has('even', item):
                self.tag_remove(('selected', '_selected'), item)
            else:
                self.tag_replace('_selected', 'selected', item)

    def get_selected(self):
        return sorted(self.tag_has('selected_odd') + self.tag_has('selected_even'))

    def set_selected(self, event):
        def selected_items():
            items = []
            window_y = int(self.root.geometry().rsplit('+', 1)[-1])
            titlebar_height = self.root.winfo_rooty() - window_y
            sw = self.select_window
            start = sw.winfo_rooty() - titlebar_height - window_y
            end = start + sw.winfo_height()

            while start < end:
                start += 1
                node = self.identify('item', event.x, start)
                if not node or node in items:
                    continue
                items.append(node)

            return sorted(items)

        def set_row_colors():
            items = self.selected_items = selected_items()

            for item in items:
                if self.tag_has('selected', item):
                    if item == self.origin_item:
                        continue

                    if self.tag_has('selected_odd', item):
                        self.tag_replace('selected_odd', 'odd', item)
                    elif self.tag_has('selected_even', item):
                        self.tag_replace('selected_even', 'even', item)

                elif self.tag_has('odd', item):
                    self.tag_replace('odd', 'selected_odd', item)
                elif self.tag_has('even', item):
                    self.tag_replace('even', 'selected_even', item)

                self.tag_add('_selected', item)

            for item in self.tag_has('_selected'):
                if item not in items:
                    self.tag_remove('_selected', item)
                    if self.tag_has('odd', item):
                        self.tag_replace('odd', 'selected_odd', item)
                    elif self.tag_has('even', item):
                        self.tag_replace('even', 'selected_even', item)
                    elif self.tag_has('selected_odd', item):
                        self.tag_replace('selected_odd', 'odd', item)
                    elif self.tag_has('selected_even', item):
                        self.tag_replace('selected_even', 'even', item)

        root_x = self.root.winfo_rootx()
        if event.x < self.origin_x:
            width = self.origin_x - event.x
            coord_x = root_x + event.x
        else:
            width = event.x - self.origin_x
            coord_x = root_x + self.origin_x

        if coord_x+width > root_x+self.winfo_width():
            width -= (coord_x+width)-(root_x+self.winfo_width())
        elif self.winfo_pointerx() < root_x:
            width -= (root_x - self.winfo_pointerx())
            coord_x = root_x

        root_y = self.winfo_rooty()
        if event.y < self.origin_y:
            height = self.origin_y - event.y
            coord_y = root_y + event.y
        else:
            height = event.y - self.origin_y
            coord_y = root_y + self.origin_y

        if coord_y+height > root_y+self.winfo_height():
            height -= (coord_y+height)-(root_y+self.winfo_height())
        elif self.winfo_pointery() < root_y + self.linespace:
            height -= (root_y - self.winfo_pointery() + self.linespace)
            coord_y = root_y + self.linespace
            if height < 0:
                height = self.winfo_rooty() + self.origin_y

        set_row_colors()
        self.select_window.geometry(f'{width}x{height}+{coord_x}+{coord_y}')


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        def print_selected_items(_):
            print(tv.get_selected())
            return 'break'

        style = self.style = ttk.Style()

        tv = Treeview(self)
        style.map("Treeview", foreground=tv.fixed_map("foreground"), background=tv.fixed_map("background"))

        tv.heading('#0', text='Name')
        tv.tag_configure('odd', background='#ffffff')
        tv.tag_configure('even', background='#aaaaaa')
        tv.tag_configure('selected_odd', background='#b0eab2')
        tv.tag_configure('selected_even', background='#25a625')

        color_tag = 'odd'
        for idx in range(0, 4):
            # Populating the tree with test data.
            color_tag = 'even' if color_tag == 'odd' else 'odd'
            tv.insert('', idx, f'{idx}', text=f'Item {idx+1}', open=1, tags=(color_tag,))
            color_tag = 'even' if color_tag == 'odd' else 'odd'
            iid = f'{idx}_{0}'
            tv.insert(f'{idx}', '0', iid, text=f'Menu {idx+1}', open=1, tags=(color_tag,))
            for i in range(0, 5):
                color_tag = 'even' if color_tag == 'odd' else 'odd'
                tv.insert(iid, i, f'{iid}_{i}', text=f'Sub item {i+1}', tags=(color_tag,))

            color_tag = 'even' if color_tag == 'odd' else 'odd'
            tv.insert(iid, 5, f'{iid}_{5}', text=f'Another Menu {idx+1}', open=1, tags=(color_tag,))
            iid = f'{iid}_{5}'
            for i in range(0, 3):
                color_tag = 'even' if color_tag == 'odd' else 'odd'
                tv.insert(iid, i, f'{iid}_{i}', text=f'Sub item {i+1}', tags=(color_tag,))

        self.title('Treeview Demo')
        self.geometry('275x650+3000+250')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        tv.config(selectmode="none")
        tv.grid(sticky='NSEW')

        button = ttk.Button(self, text='Get Selected Items')
        button.grid()
        button.bind('<Button-1>', print_selected_items)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()