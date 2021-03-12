import random
import sys
import typing

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QCheckBox, QVBoxLayout, QPushButton, QFrame, QLineEdit, QMessageBox, \
    QWidget, QHBoxLayout
from data_randomiser import run as data_run
from resource_randomiser import run as res_run

app = QApplication([])
base = QFrame()
base.setWindowTitle("Minecraft Randomizer")
base.setStyleSheet("background-image: url(icons/bg.png); color: black;")
base.setWindowIcon(QIcon("icons/advancements.png"))
layout = QVBoxLayout()


class IconLabel(QWidget):
    size = QSize(16, 16)
    spacing = 2

    def __init__(self, icon_name, text, final_stretch=True):
        super().__init__()

        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_layout)

        icon = QLabel()
        icon.setPixmap(QIcon(f"icons/{icon_name}.png").pixmap(self.size))

        if icon_name == "seed":
            _layout.addSpacing(3)
        _layout.addWidget(icon)
        spacing = self.spacing
        if icon_name == "seed":
            spacing += 3
        _layout.addSpacing(spacing)
        _layout.addWidget(QLabel(text))

        if final_stretch:
            _layout.addStretch()


_seed_label = IconLabel("seed", "Seed")
_s = QLineEdit()
_folder_label = IconLabel("pack", "Folder")
_f = QLineEdit()
layout.addWidget(_seed_label)
layout.addWidget(_s)
layout.addWidget(_folder_label)
layout.addWidget(_f)


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Tab:
    def __init__(self, name: str, options: typing.List[str], func: typing.Callable):
        self.func = func
        self.name = name
        label = QLabel(name)
        layout.addWidget(label)
        self.buttons: typing.Dict[str, QCheckBox] = {}
        for opt in options:
            optkey = opt.replace(' ', '').lower()
            chkbx = QCheckBox(opt, base)
            # chkbx.setStyleSheet("color: white;")
            chkbx.setIcon(QIcon(f"icons/{optkey}.png"))
            self.buttons[optkey] = chkbx
            layout.addWidget(chkbx)
        submit = QPushButton("Randomize", base)
        layout.addWidget(submit)
        submit.clicked.connect(self.submitted)

    def submitted(self):
        folder = _s.text() or ('data' if self.name == "Data" else 'pack')
        seed = _f.text() or random.randrange(sys.maxsize)
        args = map(lambda x: x.isChecked(), self.buttons.values())
        output = self.func(folder, seed, *args)
        c_menu = QMessageBox()
        c_menu.setText(output)
        c_menu.exec()
        app.exit()


data_button = Tab("Data", ["Advancements", "Loot Tables", "Recipes", "Structures", "Tags", "Preserve Chances"], data_run)
layout.addWidget(QHLine())
res_button = Tab("Resource", ["Textures", "Models", "Block States", "Sounds", "Texts", "Fonts", "Shaders"], res_run)

base.setLayout(layout)
base.show()
app.exec()
