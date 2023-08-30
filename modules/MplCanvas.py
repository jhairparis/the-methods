from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import darkdetect


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor="none")

        self.axes = fig.add_subplot(111)

        self.axes.set_facecolor("none")
        self.axes.spines["top"].set_color("none")
        self.axes.spines["right"].set_color("none")

        if darkdetect.isDark() == True:
            self.axes.spines["bottom"].set_color("white")
            self.axes.spines["left"].set_color("white")
            self.axes.tick_params(axis="x", colors="white")
            self.axes.tick_params(axis="y", colors="white")

        super(MplCanvas, self).__init__(fig)
