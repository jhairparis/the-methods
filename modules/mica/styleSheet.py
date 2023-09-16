from modules.mica.theme.dark import darkSheet
from modules.mica.theme.light import lightSheet
from modules.mica.theme.getAccent import getAccent
from modules.mica.blurWindow import GlobalBlur
from win32mica import ApplyMica, MICAMODE
import darkdetect


def setMicaWindow(root):
    hwnd = root.winId().__int__()

    mode = MICAMODE.DARK
    mode = MICAMODE.LIGHT
    mode = darkdetect.isDark()

    ApplyMica(hwnd, mode)


def setStyleSheet(root):
    accent = getAccent()

    if darkdetect.isDark() == True:
        root.setStyleSheet(darkSheet(accent))
    else:
        root.setStyleSheet(lightSheet(accent))


def ApplyMenuBlur(hwnd: int):
    hwnd = int(hwnd)

    if darkdetect.isDark() == True:
        GlobalBlur(
            hwnd,
            Acrylic=True,
            hexColor="#21212140",
            Dark=True,
            smallCorners=True,
        )
    else:
        GlobalBlur(
            hwnd,
            Acrylic=True,
            hexColor="#faf7f740",
            Dark=True,
            smallCorners=True,
        )
