from PyQt5 import QtCore, QtGui, QtWidgets
from view import View

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = View()
    ui.setupUi(MainWindow)
    ui.on_setup_complete()
    MainWindow.show()

    sys.exit(app.exec_())
