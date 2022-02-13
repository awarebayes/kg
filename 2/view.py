from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from model import Model

class Canvas(QtWidgets.QFrame):

    def __init__(self, parent):
        super(Canvas, self).__init__(parent=parent)
        self.setMinimumSize(QtCore.QSize(451, 461))
        self.setMouseTracking(True)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame")

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(event, qp)
        qp.end()

    def draw(self, event, qp):



class View(object):

    def __init__(self, controller):
        self.controller = controller

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 882)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.showSlidersCB = QtWidgets.QCheckBox(self.centralwidget)
        self.showSlidersCB.setChecked(True)
        self.showSlidersCB.setObjectName("showSlidersCB")
        self.verticalLayout.addWidget(self.showSlidersCB)
        self.ShowBaseFigures = QtWidgets.QCheckBox(self.centralwidget)
        self.ShowBaseFigures.setObjectName("ShowBaseFigures")
        self.verticalLayout.addWidget(self.ShowBaseFigures)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setMinimumSize(QtCore.QSize(331, 225))
        self.page.setObjectName("page")
        self.formLayoutWidget = QtWidgets.QWidget(self.page)
        self.formLayoutWidget.setGeometry(QtCore.QRect(1, 1, 331, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.formLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.TransYLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.TransYLabel.setObjectName("TransYLabel")
        self.gridLayout.addWidget(self.TransYLabel, 1, 0, 1, 1)
        self.TransXLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.TransXLabel.setObjectName("TransXLabel")
        self.gridLayout.addWidget(self.TransXLabel, 0, 0, 1, 1)
        self.TransYSlider = QtWidgets.QSlider(self.formLayoutWidget)
        self.TransYSlider.setOrientation(QtCore.Qt.Horizontal)
        self.TransYSlider.setObjectName("TransYSlider")
        self.gridLayout.addWidget(self.TransYSlider, 1, 1, 1, 1)
        self.RotateSlider = QtWidgets.QSlider(self.formLayoutWidget)
        self.RotateSlider.setMinimum(-180)
        self.RotateSlider.setMaximum(180)
        self.RotateSlider.setOrientation(QtCore.Qt.Horizontal)
        self.RotateSlider.setObjectName("RotateSlider")
        self.gridLayout.addWidget(self.RotateSlider, 3, 1, 1, 1)
        self.ScaleSlider = QtWidgets.QSlider(self.formLayoutWidget)
        self.ScaleSlider.setMinimum(1)
        self.ScaleSlider.setMaximum(99)
        self.ScaleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ScaleSlider.setInvertedAppearance(False)
        self.ScaleSlider.setInvertedControls(False)
        self.ScaleSlider.setObjectName("ScaleSlider")
        self.gridLayout.addWidget(self.ScaleSlider, 2, 1, 1, 1)
        self.TransXSlider = QtWidgets.QSlider(self.formLayoutWidget)
        self.TransXSlider.setOrientation(QtCore.Qt.Horizontal)
        self.TransXSlider.setObjectName("TransXSlider")
        self.gridLayout.addWidget(self.TransXSlider, 0, 1, 1, 1)
        self.ScaleLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.ScaleLabel.setObjectName("ScaleLabel")
        self.gridLayout.addWidget(self.ScaleLabel, 2, 0, 1, 1)
        self.RotateLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.RotateLabel.setObjectName("RotateLabel")
        self.gridLayout.addWidget(self.RotateLabel, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setMinimumSize(QtCore.QSize(331, 225))
        self.page_2.setObjectName("page_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.page_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 331, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TransXLabel1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.TransXLabel1.setObjectName("TransXLabel1")
        self.gridLayout_2.addWidget(self.TransXLabel1, 0, 0, 1, 1)
        self.RotateLabel1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RotateLabel1.setObjectName("RotateLabel1")
        self.gridLayout_2.addWidget(self.RotateLabel1, 3, 0, 1, 1)
        self.TransYLabel1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.TransYLabel1.setObjectName("TransYLabel1")
        self.gridLayout_2.addWidget(self.TransYLabel1, 1, 0, 1, 1)
        self.TransScaleLabel1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.TransScaleLabel1.setObjectName("TransScaleLabel1")
        self.gridLayout_2.addWidget(self.TransScaleLabel1, 2, 0, 1, 1)
        self.TransXSB = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.TransXSB.setMaximum(1.0)
        self.TransXSB.setSingleStep(0.05)
        self.TransXSB.setObjectName("TransXSB")
        self.gridLayout_2.addWidget(self.TransXSB, 0, 1, 1, 1)
        self.TransYSB = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.TransYSB.setMaximum(1.0)
        self.TransYSB.setSingleStep(0.05)
        self.TransYSB.setObjectName("TransYSB")
        self.gridLayout_2.addWidget(self.TransYSB, 1, 1, 1, 1)
        self.ScaleSB = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.ScaleSB.setMinimum(0.1)
        self.ScaleSB.setMaximum(5.0)
        self.ScaleSB.setSingleStep(0.5)
        self.ScaleSB.setProperty("value", 1.0)
        self.ScaleSB.setObjectName("ScaleSB")
        self.gridLayout_2.addWidget(self.ScaleSB, 2, 1, 1, 1)
        self.RotateSB = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.RotateSB.setMinimum(-180.0)
        self.RotateSB.setMaximum(180.0)
        self.RotateSB.setSingleStep(10.0)
        self.RotateSB.setObjectName("RotateSB")
        self.gridLayout_2.addWidget(self.RotateSB, 3, 1, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.frame = Canvas(MainWindow)
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def register_controller_callbacks(self):
        self.showSlidersCB.stateChanged.connect(self.controller.toggle_sliders)
        self.ShowBaseFigures.stateChanged.connect(self.controller.show_base_figures)

        self.TransXSB.valueChanged.connect(self.controller.change_trans_x)
        self.TransYSB.valueChanged.connect(self.controller.change_trans_y)

        self.TransXSlider.valueChanged.connect(self.controller.change_trans_x_slider)
        self.TransYSlider.valueChanged.connect(self.controller.change_trans_y_slider)

        self.ScaleSB.valueChanged.connect(self.controller.change_scale)
        self.ScaleSlider.valueChanged.connect(self.controller.change_scale_slider)

        self.RotateSB.valueChanged.connect(self.controller.change_rotate)
        self.RotateSlider.valueChanged.connect(self.controller.change_rotate)

    def toggle_silders(self, value):
        value = 1 - int(value)
        self.stackedWidget.setCurrentIndex(value)

    def adjust_trans_x_components(self, value):
        self.TransXSB.setValue(value)
        value = int(value * 100)
        self.TransXSlider.setValue(value)

    def adjust_trans_y_components(self, value):
        self.TransYSB.setValue(value)
        value = int(value * 100)
        self.TransYSlider.setValue(value)

    def adjust_scale_components(self, value):
        value = round(value, 1)
        self.ScaleSB.setValue(value)

        norm = (value - 0.1) / 4.9
        val_1_100 = int(100 * norm)

        self.ScaleSlider.setValue(val_1_100)

    def adjust_rotate_components(self, value):
        self.RotateSB.setValue(value)
        value = int(value)
        self.RotateSlider.setValue(value)

    def register_model_callbacks(self, model: Model):
        model.add_callback('show_sliders', self.toggle_silders)
        model.add_callback('trans_x', self.adjust_trans_x_components)
        model.add_callback('trans_y', self.adjust_trans_y_components)
        model.add_callback('scale', self.adjust_scale_components)
        model.add_callback('rotate', self.adjust_rotate_components)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.showSlidersCB.setText(_translate("MainWindow", "Show sliders"))
        self.ShowBaseFigures.setText(_translate("MainWindow", "Show base figures"))
        self.TransYLabel.setText(_translate("MainWindow", "Translate Y"))
        self.TransXLabel.setText(_translate("MainWindow", "Translate X"))
        self.ScaleLabel.setText(_translate("MainWindow", "Scale"))
        self.RotateLabel.setText(_translate("MainWindow", "Rotate (deg)"))
        self.TransXLabel1.setText(_translate("MainWindow", "Translate X"))
        self.RotateLabel1.setText(_translate("MainWindow", "Rotate (deg)"))
        self.TransYLabel1.setText(_translate("MainWindow", "Translate Y"))
        self.TransScaleLabel1.setText(_translate("MainWindow", "Scale"))
        self.frame.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Canvas</p></body></html>"))
