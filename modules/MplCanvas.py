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
        self.accent = rgb2hex(theme["palette"][0])

        if darkdetect.isDark() == True:
            self.axes.spines["bottom"].set_color(self.accent)
            self.axes.spines["left"].set_color(self.accent)
            self.axes.tick_params(axis="x", colors=self.accent)
            self.axes.tick_params(axis="y", colors=self.accent)
            self.axes.title.set_color(self.accent)

        super(MplCanvas, self).__init__(self.fig)

    def draw(self):
        if darkdetect.isDark() == True:
            self.axes.title.set_color(self.accent)

        return super().draw()
