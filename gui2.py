from PyQt5.QtWidgets import QApplication, QLabel, QCheckBox, QWidget, QVBoxLayout, QHBoxLayout

app = QApplication([])
base = QWidget()
base.setStyleSheet("background-image: url(bg.png);")
layout = QVBoxLayout()

_b = QWidget()
bars = QHBoxLayout()

bars.addWidget(QLabel("Data"))
bars.addWidget(QLabel("Resource"))

_b.setLayout(bars)
layout.addWidget(_b)

layout.addWidget(QLabel("hi", base))
checkbox = QCheckBox("bbbb", base)
layout.addWidget(checkbox)

base.setLayout(layout)
base.show()
app.exec()
