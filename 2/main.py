# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from view import View
from model import Model
from controller import Controller


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    controller = Controller()
    model = Model()
    view = View(controller)

    controller.set_model(model)
    controller.set_view(view)

    view.setupUi(MainWindow)
    view.register_controller_callbacks()
    view.register_view_callbacks(model)

    MainWindow.show()
    sys.exit(app.exec_())
