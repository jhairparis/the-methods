from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from modules.mica.theme.getTheme import getTheme, rgb2hex
import darkdetect


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="none")

        self.axes = self.fig.add_subplot(111)

        self.axes.set_facecolor("none")
        self.axes.spines["top"].set_color("none")
        self.axes.spines["right"].set_color("none")

        theme = getTheme()
        accent = rgb2hex(theme["palette"][0])

        if darkdetect.isDark() == True:
            self.axes.spines["bottom"].set_color(accent)
            self.axes.spines["left"].set_color(accent)
            self.axes.tick_params(axis="x", colors=accent)
            self.axes.tick_params(axis="y", colors=accent)

        super(MplCanvas, self).__init__(self.fig)
