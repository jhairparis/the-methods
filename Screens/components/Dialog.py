from PySide2.QtWidgets import QDialog, QWidget
from modules.mica.styleSheet import setMicaWindow, setStyleSheet
from PySide2.QtCore import Qt


class Dialog(QDialog):
    def __init__(self, parent: QWidget, auto: bool):
        if not auto:
            super().__init__(parent)
        else:
            super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        setMicaWindow(self)
        setStyleSheet(self)
