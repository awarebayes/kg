import sys
from my_gui import *

app, application = None, None

BASIC_LINE = 0
HOR_VER_LINE = 1


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)

    def mousePressEvent(self, event):
        maybe_xy = self.ui.transform(event.pos().x(), event.pos().y())
        if not maybe_xy:
            return
        x, y = maybe_xy
        print("points ", x, y)

        if event.button() == Qt.LeftButton:
            self.ui.draw_line(x, y, BASIC_LINE)
        elif event.button() == Qt.RightButton:
            self.ui.draw_line(x, y, HOR_VER_LINE)


def main():
    global app, application
    app = QtWidgets.QApplication([])
    application = MainWin()
    application.show()

    sys.exit(app.exec())


main()
