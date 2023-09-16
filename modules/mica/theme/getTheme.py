from winreg import *
import re


def getTheme():
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

    value = QueryValueEx(key, "AccentPalette")
    palette = [
        int.from_bytes(value[0][i : i + 1], byteorder="little")
        for i in range(0, len(value[0]), 1)
    ]
    palette = [palette[i : i + 4] for i in range(0, len(palette), 4)]
    palette = [f"rgb{tuple(map(int, g[:3]))}" for g in palette]

    return {"accent": accent, "palette": palette}


def rgb2hex(value: str) -> str:
    numbers = re.findall(r"\d+", value)
    numbers = tuple(map(int, numbers))

    return "#{:02x}{:02x}{:02x}".format(numbers[0], numbers[1], numbers[2])
