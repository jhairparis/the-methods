from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from winreg import *
import time
import numpy as np
from lib.Logic import Logic
from modules.MplCanvas import MplCanvas

from icons import stylelight_rc

from modules.TableModel import TableModel
from pandas import DataFrame

registry = ConnectRegistry(None, HKEY_CURRENT_USER)
key = OpenKey(
    registry, r"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Explorer\\Accent"
)
key_value = QueryValueEx(key, "AccentColorMenu")
accent_int = key_value[0]
accent = accent_int - 4278190080
accent = str(hex(accent)).split("x")[1]
accent = accent[4:6] + accent[2:4] + accent[0:2]
accent = "rgb" + str(tuple(int(accent[i : i + 2], 16) for i in (0, 2, 4)))


class Ui_MainWindow(object):
    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        self.graph_line.set_data(t, np.sin(t + time.time()))
        self.graph_line.figure.canvas.draw()

    def setupUi(self, MainWindow):
        self.logic = Logic()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(980, 700)
        MainWindow.setMinimumSize(QtCore.QSize(980, 700))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(
            """/*BACKGROUND*/
QWidget {
    background: transparent;
    color: rgb(0, 0, 0);
    font-size: 17px;
    font-family: "Segoe UI Variable Small", serif;
    font-weight: 400;
}

/*MENU*/
QMenuBar {
    background-color: transparent;
    color: rgba(0, 0, 0);
    padding: 10px;
    font-size: 17px;
    font-family: "Segoe UI Variable Small", serif;
    font-weight: 400;
}

QMenuBar::item {
    background-color: transparent;
    padding: 10px 13px;
    margin-left: 5px;
    border-radius: 5px;
}

QMenuBar::item:selected {
    background-color: rgb(0, 0, 0, 10);
}

QMenuBar::item:pressed {
    background-color: rgb(0, 0, 0, 7);
    color: rgb(0, 0, 0, 150);
}

QMenu {
    background-color: transparent;
    padding-left: 1px;
    padding-top: 1px;
    border-radius: 5px;
    border: 1px solid rgb(0, 0, 0, 13);
}

QMenu::item {
    background-color: transparent;
    padding: 5px 15px;
    border-radius: 5px;
    min-width: 60px;
    margin: 3px;
}

QMenu::item:selected {
    background-color: rgb(0, 0, 0, 10);
}

QMenu::item:pressed {
    background-color: rgb(0, 0, 0, 7);
}

QMenu::right-arrow {
    image: url(:/newPrefix/img light/TreeViewClose.png);
    min-width: 40px;
    min-height: 18px;
}

QMenuBar:disabled {
    color: rgb(0, 0, 0, 150);
}

QMenu::item:disabled {
    color: rgb(0, 0, 0, 150);
    background-color: transparent;
}

/*PUSHBUTTON*/
QPushButton {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 7px;
    min-height: 38px;
    max-height: 38px;
}

QPushButton:hover {
    background-color: rgb(0, 0, 0, 10);
    border: 1px solid rgb(0, 0, 0, 13);
}

QPushButton::pressed {
    color: rgb(0, 0, 0, 150);
}

QPushButton::disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

/*RADIOBUTTON*/
QRadioButton {
    min-height: 30px;
    max-height: 30px;
}

QRadioButton::indicator {
    width: 22px;
    height: 22px;
    border-radius: 13px;
    border: 2px solid #999999;
    background-color: rgb(0, 0, 0, 5);
    margin-right: 5px;
}

QRadioButton::indicator:hover {
    background-color: rgb(0, 0, 0, 0);
}

QRadioButton::indicator:pressed {
    background-color: rgb(0, 0, 0, 5);
    border: 2px solid #bbbbbb;
    image: url(:/RadioButton/img light/RadioButton.png);
}

QRadioButton::indicator:checked {
    background-color: """
            + accent
            + """;
    border: 2px solid """
            + accent
            + """;
    image: url(:/RadioButton/img light/RadioButton.png);
    color: rgb(255, 255, 255);
}

QRadioButton::indicator:checked:hover {
    image: url(:/RadioButton/img light/RadioButtonHover.png);
}

QRadioButton::indicator:checked:pressed {
    image: url(:/RadioButton/img light/RadioButtonPressed.png);
}

QRadioButton:disabled {
    color: rgb(0, 0, 0, 110);
}

QRadioButton::indicator:disabled {
    border: 2px solid #bbbbbb;
    background-color: rgb(0, 0, 0, 0);
}

/*CHECKBOX*/
QCheckBox {
    min-height: 30px;
    max-height: 30px;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 5px;
    border: 2px solid #999999;
    background-color: rgb(0, 0, 0, 0);
    margin-right: 5px;
}

QCheckBox::indicator:hover {
    background-color: rgb(0, 0, 0, 15);
}

QCheckBox::indicator:pressed {
    background-color: rgb(0, 0, 0, 24);
    border: 2px solid #bbbbbb;
}

QCheckBox::indicator:checked {
    background-color: """
            + accent
            + """;
    border: 2px solid """
            + accent
            + """;
    image: url(:/CheckBox/img light/CheckBox.png);
    color: rgb(255, 255, 255);
}

QCheckBox::indicator:checked:pressed {
    image: url(:/CheckBox/img light/CheckBoxPressed.png);
}

QCheckBox:disabled {
    color: rgb(0, 0, 0, 110);
}

QCheckBox::indicator:disabled {
    border: 2px solid #bbbbbb;
    background-color: rgb(0, 0, 0, 0);
}

/*GROUPBOX*/
QGroupBox {
    border-radius: 5px;
    border: 1px solid rgb(0, 0, 0, 13);
    margin-top: 36px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    background-color: rgb(0, 0, 0, 10);
    padding: 7px 15px;
    margin-left: 5px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QGroupBox::title::disabled {
    color: rgb(0, 0, 0, 150);
}

/*TABWIDGET*/
QTabWidget {
}

QWidget {
    border-radius: 5px;
}

QTabWidget::pane {
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
}

QTabWidget::tab-bar {
    left: 5px;
}

QTabBar::tab {
    background-color: rgb(0, 0, 0, 0);
    padding: 7px 15px;
    margin-right: 2px;
}

QTabBar::tab:hover {
    background-color: rgb(0, 0, 0, 13);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: rgb(0, 0, 0, 10);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:disabled {
    color: rgb(0, 0, 0, 150)
}

/*SPINBOX*/
QSpinBox {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
    padding-left: 10px;
    min-height: 38px;
    max-height: 38px;
    min-width: 100px;
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QSpinBox:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QSpinBox::focus {
    background-color: rgb(0, 0, 0, 5);
    border: 1px solid rgb(0, 0, 0, 10);
    color: rgb(0, 0, 0, 200);
    border-bottom: 2px solid """
            + accent
            + """;
}

QSpinBox::up-button {
    image: url(:/SpinBox/img light/SpinBoxUp.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QSpinBox::up-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QSpinBox::up-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QSpinBox::down-button {
    image: url(:/SpinBox/img light/SpinBoxDown.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QSpinBox::down-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QSpinBox::down-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QSpinBox::drop-down {
    background-color: transparent;
    width: 50px;
}

QSpinBox:disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

QSpinBox::up-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxUpDisabled.png);
}

QSpinBox::down-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxDownDisabled.png);
}

/*DOUBLESPINBOX*/
QDoubleSpinBox {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
    padding-left: 10px;
    min-height: 38px;
    max-height: 38px;
    min-width: 100px;
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QDoubleSpinBox:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QDoubleSpinBox::focus {
    background-color: rgb(0, 0, 0, 5);
    border: 1px solid rgb(0, 0, 0, 10);
    color: rgb(0, 0, 0, 200);
    border-bottom: 2px solid """
            + accent
            + """;
}

QDoubleSpinBox::up-button {
    image: url(:/SpinBox/img light/SpinBoxUp.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QDoubleSpinBox::up-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QDoubleSpinBox::up-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QDoubleSpinBox::down-button {
    image: url(:/SpinBox/img light/SpinBoxDown.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QDoubleSpinBox::down-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QDoubleSpinBox::down-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QDoubleSpinBox::drop-down {
    background-color: transparent;
    width: 50px;
}

QDoubleSpinBox:disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

QDoubleSpinBox::up-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxUpDisabled.png);
}

QDoubleSpinBox::down-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxDownDisabled.png);
}

/*DATETIMEEDIT*/
QDateTimeEdit {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
    padding-left: 10px;
    min-height: 38px;
    max-height: 38px;
    min-width: 100px;
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QDateTimeEdit:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QDateTimeEdit::focus {
    background-color: rgb(0, 0, 0, 5);
    border: 1px solid rgb(0, 0, 0, 10);
    color: rgb(0, 0, 0, 200);
    border-bottom: 2px solid """
            + accent
            + """;
}

QDateTimeEdit::up-button {
    image: url(:/SpinBox/img light/SpinBoxUp.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QDateTimeEdit::up-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QDateTimeEdit::up-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QDateTimeEdit::down-button {
    image: url(:/SpinBox/img light/SpinBoxDown.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QDateTimeEdit::down-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QDateTimeEdit::down-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QDateTimeEdit::drop-down {
    background-color: transparent;
    width: 50px;
}

QDateTimeEdit:disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

QDateTimeEdit::up-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxUpDisabled.png);
}

QDateTimeEdit::down-button:disabled {
    image: url(:/SpinBox/img light/SpinBoxDownDisabled.png);
}

/*SLIDERVERTICAL*/
QSlider:vertical {
    min-width: 30px;
    min-height: 100px;
}

QSlider::groove:vertical {
    width: 5px; 
    background-color: rgb(0, 0, 0, 100);
    border-radius: 2px;
}

QSlider::handle:vertical {
    background-color: """
            + accent
            + """;
    border: 6px solid #dbdbdb;
    height: 13px;
    min-width: 15px;
    margin: 0px -10px;
    border-radius: 12px;
}

QSlider::handle:vertical:hover {
    background-color: """
            + accent
            + """;
    border: 4px solid #dbdbdb;
    height: 17px;
    min-width: 15px;
    margin: 0px -10px;
    border-radius: 12px
}

QSlider::handle:vertical:pressed {
    background-color: """
            + accent
            + """;
    border: 7px solid #dbdbdb;
    height: 11px;
    min-width: 15px;
    margin: 0px -10px;
    border-radius: 12px
}

QSlider::groove:vertical:disabled {
    background-color: rgb(0, 0, 0, 75);
}

QSlider::handle:vertical:disabled {
    background-color: #808080;
    border: 6px solid #cccccc;
}

/*SLIDERHORIZONTAL*/
QSlider:horizontal {
    min-width: 100px;
    min-height: 30px;
}

QSlider::groove:horizontal {
    height: 5px; 
    background-color: rgb(0, 0, 0, 100);
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: """
            + accent
            + """;
    border: 6px solid #dbdbdb;
    width: 13px;
    min-height: 15px;
    margin: -10px 0;
    border-radius: 12px
}

QSlider::handle:horizontal:hover {
    background-color: """
            + accent
            + """;
    border: 4px solid #dbdbdb;
    width: 17px;
    min-height: 15px;
    margin: -10px 0;
    border-radius: 12px
}

QSlider::handle:horizontal:pressed {
    background-color: """
            + accent
            + """;
    border: 7px solid #dbdbdb;
    width: 11px;
    min-height: 15px;
    margin: -10px 0;
    border-radius: 12px
}

QSlider::groove:horizontal:disabled {
    background-color: rgb(0, 0, 0, 75);
}

QSlider::handle:horizontal:disabled {
    background-color: #808080;
    border: 6px solid #cccccc;
}

/*PROGRESSBAR*/
QProgressBar {
    background-color: qlineargradient(spread:reflect, x1:0.5, y1:0.5, x2:0.5, y2:1, stop:0.233831 rgba(0, 0, 0, 255), stop:0.343284 rgba(0, 0, 0, 0));
    border-radius: 2px;
    min-height: 4px;
    max-height: 4px;
}

QProgressBar::chunk {
    background-color: """
            + accent
            + """;
    border-radius: 2px;
}

/*COMBOBOX*/
QComboBox {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
    padding-left: 10px;
    min-height: 38px;
    max-height: 38px;
}

QComboBox:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
}

QComboBox::pressed {
    border: 1px solid rgb(0, 0, 0, 10);
}

QComboBox::down-arrow {
    image: url(:/newPrefix/img light/ComboBox.png);
}

QComboBox::drop-down {
    background-color: transparent;
    min-width: 50px;
}

QComboBox:disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

QComboBox::down-arrow:disabled {
    image: url(:/newPrefix/img light/ComboBoxDisabled.png);
}

/*LINEEDIT*/
QLineEdit {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    font-size: 16px;
    font-family: "Segoe UI", serif;
    font-weight: 500;
    border-radius: 7px;
    border-bottom: 1px solid rgb(0, 0, 0, 100);
    padding-top: 0px;
    padding-left: 5px;
}

QLineEdit:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QLineEdit:focus {
    border-bottom: 2px solid """
            + accent
            + """;
    background-color: rgb(0, 0, 0, 5);
    border-top: 1px solid rgb(0, 0, 0, 13);
    border-left: 1px solid rgb(0, 0, 0, 13);
    border-right: 1px solid rgb(0, 0, 0, 13);
}

QLineEdit:disabled {
    color: rgb(0, 0, 0, 150);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

/*SCROLLVERTICAL*/
QScrollBar:vertical {
    border: 6px solid rgb(0, 0, 0, 0);
    margin: 14px 0px 14px 0px;
    width: 16px;
}

QScrollBar:vertical:hover {
    border: 5px solid rgb(0, 0, 0, 0);
}

QScrollBar::handle:vertical {
    background-color: rgb(0, 0, 0, 110);
    border-radius: 2px;
    min-height: 25px;
}

QScrollBar::sub-line:vertical {
    image: url(:/ScrollVertical/img light/ScrollTop.png);
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover {
    image: url(:/ScrollVertical/img light/ScrollTopHover.png);
}

QScrollBar::sub-line:vertical:pressed {
    image: url(:/ScrollVertical/img light/ScrollTopPressed.png);
}

QScrollBar::add-line:vertical {
    image: url(:/ScrollVertical/img light/ScrollBottom.png);
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover {
    image: url(:/ScrollVertical/img light/ScrollBottomHover.png);
}

QScrollBar::add-line:vertical:pressed {
    image: url(:/ScrollVertical/img light/ScrollBottomPressed.png);
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

/*SCROLLHORIZONTAL*/
QScrollBar:horizontal {
    border: 6px solid rgb(0, 0, 0, 0);
    margin: 0px 14px 0px 14px;
    height: 16px;
}

QScrollBar:horizontal:hover {
    border: 5px solid rgb(0, 0, 0, 0);
}

QScrollBar::handle:horizontal {
    background-color: rgb(0, 0, 0, 110);
    border-radius: 2px;
    min-width: 25px;
}

QScrollBar::sub-line:horizontal {
    image: url(:/ScrollHorizontal/img light/ScrollLeft.png);
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover {
    image: url(:/ScrollHorizontal/img light/ScrollLeftHover.png);
}

QScrollBar::sub-line:horizontal:pressed {
    image: url(:/ScrollHorizontal/img light/ScrollLeftPressed.png);
}

QScrollBar::add-line:horizontal {
    image: url(:/ScrollHorizontal/img light/ScrollRight.png);
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover {
    image: url(:/ScrollHorizontal/img light/ScrollRightHover.png);
}

QScrollBar::add-line:horizontal:pressed {
    image: url(:/ScrollHorizontal/img light/ScrollRightPressed.png);
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

/*TEXTEDIT*/
QTextEdit {
    background-color: rgb(0, 0, 0, 7);
    border: 1px solid rgb(0, 0, 0, 13);
    font-size: 16px;
    font-family: "Segoe UI", serif;
    font-weight: 500;
    border-radius: 7px;
    border-bottom: 1px solid rgb(0, 0, 0, 100);
    padding: 5px;
}

QTextEdit:hover {
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 1px solid rgb(0, 0, 0, 100);
}

QTextEdit:focus {
    background-color: rgb(0, 0, 0, 5);
    border-top: 1px solid rgb(0, 0, 0, 13);
    border-left: 1px solid rgb(0, 0, 0, 13);
    border-right: 1px solid rgb(0, 0, 0, 13);
    border-bottom: 2px solid """
            + accent
            + """;
}

QTextEdit:disabled {
    color: rgb(0, 0, 0, 110);
    background-color: rgb(0, 0, 0, 13);
    border: 1px solid rgb(0, 0, 0, 5);
}

/*CALENDAR*/
QCalendarWidget {
}

QCalendarWidget QToolButton {
    height: 36px;
    font-size: 18px;
    background-color: rgb(0, 0, 0, 0);
    margin: 5px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar { 
    background-color: rgb(0, 0, 0, 0); 
    border: 1px solid rgb(0, 0, 0, 13);
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
    border-bottom: none;
}

QCalendarWidget QMenu {
    background-color : #f3f3f3;
}

#qt_calendar_prevmonth {
    qproperty-icon: url(:/PrevNext/img light/PrevMonth.png);
    width: 32px;
}

#qt_calendar_nextmonth {
    qproperty-icon: url(:/PrevNext/img light/NextMonth.png);
    width: 32px;
}

#qt_calendar_prevmonth:hover, #qt_calendar_nextmonth:hover {
    background-color: rgb(0, 0, 0, 10);
    border-radius: 5px;
}

#qt_calendar_prevmonth:pressed, #qt_calendar_nextmonth:pressed {
    background-color: rgb(0, 0, 0, 7);
    border-radius: 5px;
}

#qt_calendar_yearbutton, #qt_calendar_monthbutton {
    color: rgb(0, 0, 0);
    margin: 5px 0px;
    padding: 0px 10px;
}

#qt_calendar_yearbutton:hover, #qt_calendar_monthbutton:hover {
    background-color: rgb(0, 0, 0, 10);
    border-radius: 5px;
}

#qt_calendar_yearbutton:pressed, #qt_calendar_monthbutton:pressed {
    background-color: rgb(0, 0, 0, 7);
    border-radius: 5px;
}

QCalendarWidget QToolButton::menu-indicator#qt_calendar_monthbutton {
    background-color: transparent;
}

QCalendarWidget QSpinBox {
    margin: 5px 0px;
}

QCalendarWidget QSpinBox::focus {
    background-color: rgb(0, 0, 0, 5);
    border: 1px solid rgb(0, 0, 0, 10);
    color: rgb(0, 0, 0, 200);
    border-bottom: 2px solid """
            + accent
            + """;
}

QCalendarWidget QSpinBox::up-button {
    image: url(:/SpinBox/img light/SpinBoxUp.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QCalendarWidget QSpinBox::up-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QCalendarWidget QSpinBox::up-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QCalendarWidget QSpinBox::down-button {
    image: url(:/SpinBox/img light/SpinBoxDown.png);
    background-color: rgb(0, 0, 0, 0);
    border: 1px solid rgb(0, 0, 0, 0);
    border-radius: 4px;
    margin-top: 1px;
    margin-bottom: 1px;
    margin-right: 2px;
    min-width: 30px;
    max-width: 30px;
    min-height: 20px;
}

QCalendarWidget QSpinBox::down-button:hover {
    background-color: rgb(0, 0, 0, 10);
}

QCalendarWidget QSpinBox::down-button:pressed {
    background-color: rgb(0, 0, 0, 5);
}

QCalendarWidget QWidget { 
    alternate-background-color: rgb(0, 0, 0, 0); 
}

QCalendarWidget QAbstractItemView:enabled {
    color: rgb(0, 0, 0);  
    selection-background-color: """
            + accent
            + """;
    selection-color: black;
    border: 1px solid rgb(0, 0, 0, 10);
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    outline: 0;
}

QCalendarWidget QAbstractItemView:disabled {
    color: rgb(30, 30, 30);  
    selection-background-color: rgb(30, 30, 30);
    selection-color: black;
    border: 1px solid rgb(0, 0, 0, 13);
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
}

#qt_calendar_yearbutton:disabled, #qt_calendar_monthbutton:disabled {
    color: rgb(0, 0, 0, 110);
}

#qt_calendar_prevmonth:disabled {
    qproperty-icon: url(:/PrevNext/img light/PrevMonthDisabled.png);
}

#qt_calendar_nextmonth:disabled {
    qproperty-icon: url(:/PrevNext/img light/NextMonthDisabled.png);
}

/*TREEWIDGET*/
QTreeView {
    background-color: transparent;
    border: 1px solid rgb(0, 0, 0, 13);
    border-radius: 5px;
    outline: 0;
    padding-right: 5px;
}

QTreeView::item {
    padding: 7px;
    margin-top: 3px;
}

QTreeView::item:selected {
    color: rgb(0, 0, 0);
    background-color: rgb(0, 0, 0, 7);
    border-radius: 5px;
    margin-bottom: 3px;
    padding-left: 0px;
}

QTreeView::item:!selected:hover {
    background-color: rgb(0, 0, 0, 13);
    border-radius: 5px;
    margin-bottom: 3px;
    padding-left: 0px;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    image: url(:/newPrefix/img light/TreeViewClose.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {
    image: url(:/newPrefix/img light/TreeViewOpen.png);
}

QTreeView:disabled {
    color: rgb(0, 0, 0, 110);
}

/*TOGGLESWITCH*/
#toggleSwitch {
    color: rgb(0, 0, 0);
    font-size: 17px;
    font-family: "Segoe UI Variable Small", serif;
    font-weight: 400;
}

#toggleSwitch::indicator {
    width: 22px;
    height: 22px;
    border-radius: 13px;
    border: 2px solid #999999;
    background-color: rgb(0, 0, 0, 0);
    image: url(:/ToggleSwitch/img light/ToggleSwitchOff.png);
    margin-right: 5px;
    padding-right: 25px;
    padding-left: 0px;
}

#toggleSwitch::indicator:hover {
    background-color: rgb(0, 0, 0, 15);
    image: url(:/ToggleSwitch/img light/ToggleSwitchOffHover.png);
}

#toggleSwitch::indicator:pressed {
    background-color: rgb(0, 0, 0, 24);
    width: 26px;
    padding-right: 21px;
    image: url(:/ToggleSwitch/img light/ToggleSwitchOffPressed.png);
}

#toggleSwitch::indicator:checked {
    background-color: """
            + accent
            + """;
    border: 2px solid """
            + accent
            + """;
    image: url(:/ToggleSwitch/img light/ToggleSwitchOn.png);
    color: rgb(255, 255, 255);
    padding-left: 25px;
    padding-right: 0px;
}

#toggleSwitch::indicator:checked:hover {
    background-color: """
            + accent
            + """;
    image: url(:/ToggleSwitch/img light/ToggleSwitchOnHover.png);
}

#toggleSwitch::indicator:checked:pressed {
    background-color: """
            + accent
            + """;
    width: 26px;
    padding-left: 21px;
    image: url(:/ToggleSwitch/img light/ToggleSwitchOnPressed.png);
}

#toggleSwitch:disabled {
    color: rgb(0, 0, 0, 110);
}

#toggleSwitch::indicator:disabled {
    border: 2px solid #bbbbbb;
    image: url(:/ToggleSwitch/img light/ToggleSwitchDisabled.png);
}

/*HYPERLINKBUTTON*/
#hyperlinkButton {
    color: """
            + accent
            + """;
    font-size: 17px;
    font-family: "Segoe UI Variable Small", serif;
    border-radius: 5px;
    background-color: rgb(0, 0, 0, 0);
    border: none;
}

#hyperlinkButton:hover {
    background-color: rgb(0, 0, 0, 10);
}

#hyperlinkButton::pressed {
    background-color: rgb(0, 0, 0, 7);
    color: """
            + accent
            + """;
}

#hyperlinkButton:disabled {
    color: rgb(0, 0, 0, 110)
}

/*LISTVIEW*/
QListView {
    background-color: transparent;
    font-size: 17px;
    font-family: "Segoe UI Variable Small", serif;
    font-weight: 400;
    padding: 7px;
    border-radius: 10px;
    outline: 0;
}

QListView::item {
    height: 35px;
}

QListView::item:selected {
    background-color: rgb(0, 0, 0, 13);
    color: black;
    border-radius: 5px;
    padding-left: 0px;
}"""
        )

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.scrollCentral = QtWidgets.QScrollArea()

        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.window = QtWidgets.QFrame(self.centralwidget)
        self.window.setEnabled(True)
        self.window.setGeometry(QtCore.QRect(19, 0, 991, 1302))
        self.window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.window.setObjectName("window")

        # Right side
        self.graph = QtWidgets.QWidget(self.window)
        self.graph.setGeometry(QtCore.QRect(0, 0, 622, 520))
        # self.graph.setStyleSheet("background:blue;")

        self.graph_ = MplCanvas()

        t = np.linspace(0, 10, 101)
        (self.graph_line,) = self.graph_.axes.plot(t, np.sin(t + time.time()))
        self.graph__timer = self.graph_.new_timer(50)
        self.graph__timer.add_callback(self._update_canvas)
        self.graph__timer.start()

        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.addWidget(self.graph_)
        # self.graph_layout.addWidget(NavigationToolbar(self.graph_, self.window))

        self.graph_control = QtWidgets.QWidget(self.window)
        self.graph_control_layout = QtWidgets.QHBoxLayout()

        self.x_left = QtWidgets.QLineEdit(self.graph_control)
        self.x_left.setEnabled(True)
        self.x_left.setMinimumSize(QtCore.QSize(95, 40))
        self.x_left.setStyleSheet("")
        self.x_left.setObjectName("x_left")

        self.x_right = QtWidgets.QLineEdit(self.graph_control)
        self.x_right.setEnabled(True)
        self.x_right.setMinimumSize(QtCore.QSize(95, 40))
        self.x_right.setStyleSheet("")
        self.x_right.setObjectName("x_right")

        self.y_up = QtWidgets.QLineEdit(self.graph_control)
        self.y_up.setEnabled(True)
        self.y_up.setMinimumSize(QtCore.QSize(95, 40))
        self.y_up.setStyleSheet("")
        self.y_up.setObjectName("y_up")

        self.y_down = QtWidgets.QLineEdit(self.graph_control)
        self.y_down.setEnabled(True)
        self.y_down.setMinimumSize(QtCore.QSize(95, 40))
        self.y_down.setStyleSheet("")
        self.y_down.setObjectName("y_up")

        self.graph_control_layout.addWidget(self.x_left)
        self.graph_control_layout.addWidget(self.x_right)
        self.graph_control_layout.addWidget(self.y_up)
        self.graph_control_layout.addWidget(self.y_down)

        self.graph_control.setLayout(self.graph_control_layout)

        self.graph_layout.addWidget(self.graph_control)

        self.graph.setLayout(self.graph_layout)

        # Left side
        self.form = QtWidgets.QWidget(self.window)
        self.form.setGeometry(QtCore.QRect(641, 0, 320, 520))
        # self.form.setStyleSheet("background:red;")

        self.label_method = QtWidgets.QLabel(self.form)
        self.label_method.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_method.setObjectName("label_method")

        self.method_box = QtWidgets.QComboBox(self.form)
        self.method_box.setEnabled(True)
        self.method_box.setToolTip("")
        self.method_box.setStatusTip("")
        self.method_box.setWhatsThis("")
        self.method_box.setAccessibleName("")
        self.method_box.setAccessibleDescription("")
        self.method_box.setStyleSheet("")
        self.method_box.setCurrentText("")
        self.method_box.setMinimumContentsLength(0)
        self.method_box.setObjectName("method_box")
        self.method_box.addItem("")
        self.method_box.addItem("")
        self.method_box.addItem("")
        self.method_box.addItem("")

        self.label_fn = QtWidgets.QLabel(self.form)
        self.label_fn.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_fn.setObjectName("label_fn")

        self.fn_box = QtWidgets.QLineEdit(self.form)
        self.fn_box.setEnabled(True)
        self.fn_box.setMinimumSize(QtCore.QSize(181, 40))
        self.fn_box.setStyleSheet("")
        self.fn_box.setObjectName("fn_box")

        self.label_iteration = QtWidgets.QLabel(self.form)
        self.label_iteration.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_iteration.setObjectName("label_iteration")

        self.iteration_box = QtWidgets.QSpinBox(self.window)
        self.iteration_box.setEnabled(True)
        self.iteration_box.setMinimum(1)
        self.iteration_box.setMaximum(1000)
        self.iteration_box.setGeometry(QtCore.QRect(50, 20, 190, 40))
        self.iteration_box.setStyleSheet("")
        self.iteration_box.setObjectName("iteration_box")

        self.label_tolerance = QtWidgets.QLabel(self.form)
        self.label_tolerance.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_tolerance.setObjectName("label_tolerance")

        self.tolerance_box = QtWidgets.QLineEdit(self.form)
        self.tolerance_box.setEnabled(True)
        self.tolerance_box.setMinimumSize(QtCore.QSize(181, 40))
        self.tolerance_box.setStyleSheet("")
        self.tolerance_box.setObjectName("tolerance_box")

        self.range = QtWidgets.QWidget(self.form)
        self.range_layout = QtWidgets.QHBoxLayout()
        self.range_layout.setContentsMargins(0, 0, 0, 0)
        self.range_layout.setSpacing(0)

        self.x0 = QtWidgets.QWidget(self.form)
        self.x0_layout = QtWidgets.QVBoxLayout()
        self.x0_layout.setSpacing(14)

        self.label_x0 = QtWidgets.QLabel(self.form)
        self.label_x0.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_x0.setObjectName("label_x0")

        self.x0_box = QtWidgets.QDoubleSpinBox(self.window)
        self.x0_box.setEnabled(True)
        self.x0_box.setMinimum(-1000)
        self.x0_box.setMaximum(1000)
        self.x0_box.setGeometry(QtCore.QRect(50, 70, 190, 40))
        self.x0_box.setStyleSheet("")
        self.x0_box.setObjectName("x0_box")

        self.x0_layout.addWidget(self.label_x0)
        self.x0_layout.addWidget(self.x0_box)

        self.x0.setLayout(self.x0_layout)

        self.x1 = QtWidgets.QWidget(self.form)
        self.x1_layout = QtWidgets.QVBoxLayout()
        self.x1_layout.setSpacing(14)

        self.label_x1 = QtWidgets.QLabel(self.form)
        self.label_x1.setStyleSheet("QLabel{font-size: 11pt;}")
        self.label_x1.setObjectName("label_x1")

        self.x1_box = QtWidgets.QDoubleSpinBox(self.form)
        self.x1_box.setEnabled(True)
        self.x1_box.setMinimum(-1000)
        self.x1_box.setMaximum(1000)
        self.x1_box.setGeometry(QtCore.QRect(50, 70, 190, 40))
        self.x1_box.setStyleSheet("")
        self.x1_box.setObjectName("x1_box")

        self.x1_layout.addWidget(self.label_x1)
        self.x1_layout.addWidget(self.x1_box)

        self.x1.setLayout(self.x1_layout)

        self.range_layout.addWidget(self.x0)
        self.range_layout.addWidget(self.x1)

        self.range.setLayout(self.range_layout)

        self.pushButton = QtWidgets.QPushButton(self.form)
        self.pushButton.setEnabled(True)
        self.pushButton.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")

        # put in layout
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setSpacing(14)

        self.form_layout.addRow(self.label_method)
        self.form_layout.addRow(self.method_box)

        self.form_layout.addRow(self.label_fn)
        self.form_layout.addRow(self.fn_box)

        self.form_layout.addRow(self.label_iteration)
        self.form_layout.addRow(self.iteration_box)

        self.form_layout.addRow(self.label_tolerance)
        self.form_layout.addRow(self.tolerance_box)

        self.form_layout.addRow(self.range)

        self.form_layout.addRow(self.pushButton)

        self.form.setLayout(self.form_layout)

        self.tableWidget = QtWidgets.QTableView(self.window)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(0, 526, 950, 500))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet(
            """
            QHeaderView::section {
            background-color: transparent;
            color: black;
            font: 14px;
            border-style: outset;
            border-width: 1px;
            border-color: black;
        }
        /*The top-left area is actually a button:*/
        QTableCornerButton::section {
            background-color:"""
            + accent
            + """;
        }
        QTableView::item:selected {
            background:"""
            + accent
            + """;
        }
        """
        )
        #  /*The lower part of the vertical header:*/
        # QHeaderView {
        # background-color: #8b8d8e;
        # }

        self.tableWidget.setObjectName("tableWidget")

        model = TableModel(DataFrame(self.logic.data))
        self.tableWidget.setModel(model)

        self.scrollCentral.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollCentral.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollCentral.setWidgetResizable(True)
        self.scrollCentral.setWidget(self.centralwidget)

        MainWindow.setCentralWidget(self.scrollCentral)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setEnabled(True)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 980, 63))
        self.menuBar.setStyleSheet("")
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setEnabled(True)
        self.menuFile.setObjectName("menuFile")
        self.actionNew = QtWidgets.QMenu(self.menuFile)
        self.actionNew.setEnabled(True)
        self.actionNew.setStyleSheet("")
        self.actionNew.setObjectName("actionNew")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setEnabled(True)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPlain_Text_Document = QtWidgets.QAction(MainWindow)
        self.actionPlain_Text_Document.setObjectName("actionPlain_Text_Document")
        self.actionRich_Text_Document = QtWidgets.QAction(MainWindow)
        self.actionRich_Text_Document.setObjectName("actionRich_Text_Document")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setEnabled(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew.addAction(self.actionPlain_Text_Document)
        self.actionNew.addAction(self.actionRich_Text_Document)
        self.menuFile.addAction(self.actionNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "The methods"))

        self.label_method.setText(_translate("MainWindow", "Select method"))
        self.label_fn.setText(
            _translate("MainWindow", "Write the function (python syntax)")
        )
        self.label_iteration.setText(_translate("MainWindow", "Iteration"))
        self.label_tolerance.setText(_translate("MainWindow", "Tolerance"))
        self.label_x0.setText(_translate("MainWindow", "X0"))
        self.label_x1.setText(_translate("MainWindow", "X1"))

        self.x_left.setPlaceholderText(_translate("MainWindow", "limit x left"))
        self.x_right.setPlaceholderText(_translate("MainWindow", "limit x right"))
        self.y_up.setPlaceholderText(_translate("MainWindow", "limit y up"))
        self.y_down.setPlaceholderText(_translate("MainWindow", "limit y down"))

        self.method_box.setItemText(0, _translate("MainWindow", "Bisection"))
        self.method_box.setItemText(1, _translate("MainWindow", "Newton"))
        self.method_box.setItemText(2, _translate("MainWindow", "Secant"))
        self.method_box.setItemText(3, _translate("MainWindow", "Point"))

        self.fn_box.setPlaceholderText(_translate("MainWindow", "x**2"))

        self.tolerance_box.setPlaceholderText(_translate("MainWindow", "1e-3"))

        self.pushButton.setText(_translate("MainWindow", "Calculate"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setTitle(_translate("MainWindow", "New"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionPlain_Text_Document.setText(_translate("MainWindow", "Project"))
        self.actionRich_Text_Document.setText(_translate("MainWindow", "Project File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+I"))
