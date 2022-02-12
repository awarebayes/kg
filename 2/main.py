
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QVBoxLayout, QHBoxLayout, QSlider, QGridLayout)
import sys


#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

In this example, we draw text in Russian Cylliric.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class Canvas(QWidget):

    def __init__(self, parent=None, width=800, height=800):
        QWidget.__init__(self, parent=parent)
        vbox = QVBoxLayout(self)
        self.text = "Canvas is here"
        self.setMinimumSize(200, 200)
        self.setMaximumSize(1000, 1000)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)


class SidePanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QGridLayout(self)

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(okButton, 0, 0)
        layout.addWidget(cancelButton, 0, 1)
        layout.addWidget(sld)

        self.setMaximumWidth(400)


class View(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        vbox = QHBoxLayout(self)
        side_panel = SidePanel(self)
        canvas = Canvas(self)
        vbox.addWidget(side_panel)
        vbox.addWidget(canvas)


def main():

    app = QApplication(sys.argv)
    ex = View()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()