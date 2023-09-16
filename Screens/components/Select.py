from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from modules.mica.styleSheet import ApplyMenuBlur


class Select(QtWidgets.QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.listview = QtWidgets.QListView()
        self.setView(self.listview)

        self.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)
        ApplyMenuBlur(self.view().window().winId().__int__())
