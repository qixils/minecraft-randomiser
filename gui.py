import typing
from tkinter import *


class App(Tk):
    width = 235
    height = 400
    button_args = {"relief": "groove"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{self.width}x{self.height}")
        self.title("Minecraft Randomizer")
        self.resizable(0, 0)

        tabs = Tabs(self, self, height=40)
        tabs.grid(row=0, column=0, sticky="nsew")
        _frames = [DataPage, ResourcePage]
        self.frames = {}
        for _f in _frames:
            frame = _f(self, self)
            self.frames[_f.__name__] = frame
            frame.grid(row=1, column=0, sticky="nsew")
        self.show_frame("DataPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


class SamplePage(Frame):
    def __init__(self, parent, controller, **kw):
        super().__init__(parent, **kw)
        self.controller = controller
        self.init()

    def init(self):
        pass


class Tabs(SamplePage):
    def init(self):
        data_label = Button(self, text="Data", width=12, height=2,
                            command=lambda: self.controller.show_frame('DataPage'))
        data_label.grid(row=0, column=0, padx=(3, 5))

        res_label = Button(self, text="Resources", width=12, height=2,
                           command=lambda: self.controller.show_frame('ResourcePage'))
        res_label.grid(row=0, column=1)


class MainPage(SamplePage):
    _row = 1

    def row(self):
        _row = self._row
        self._row += 1
        return _row

    def header(self):
        label = Label(self, text="Please select the features\nyou wish to randomize")
        label.grid(row=self.row(), column=0, columnspan=2, rowspan=2, pady=(10, 10))
        self.row()

    def render_options(self, data: typing.List[str]):
        output = {}
        for label in data:
            var = BooleanVar()
            var.set(True)
            bttn = Checkbutton(self, variable=var, text=label)
            bttn.grid(row=self.row(), column=0, columnspan=2)
            output[label.replace(' ', '').lower()] = var
        return output

    def seed(self):
        label = Label(self, text="Seed")
        button = Entry(self)
        label.grid(row=0, column=0, pady=(5, 0))
        button.grid(row=0, column=1, pady=(5, 0))
        return button

    def submit(self, data: typing.Dict[str, Variable], seed: Entry, method: typing.Callable):
        button = Button(self, text="Submit", command=lambda: method(seed.get(), **{k: v.get() for k, v in data.items()}))
        button.grid(row=self.row(), column=0, rowspan=2, columnspan=2)


class DataPage(MainPage):
    def init(self):
        seed = self.seed()
        self.header()
        options = self.render_options([
            "Textures",  # TODO: dropdown options for this one ..
            "Block States",
            "Sounds",
            "Texts",
            "Fonts",
            "Shaders",
            "Models"
        ])
        self.submit(options, seed, dummy)


class ResourcePage(MainPage):
    def init(self):
        seed = self.seed()
        self.header()
        options = self.render_options([
            "Advancements",
            "Loot Tables",
            "Preserve Chances",
            "Recipes",
            "Tags",
            "Structures"
        ])
        self.submit(options, seed, dummy)


def dummy(seed, **kw):
    pass


if __name__ == '__main__':
    app = App()
    app.mainloop()
