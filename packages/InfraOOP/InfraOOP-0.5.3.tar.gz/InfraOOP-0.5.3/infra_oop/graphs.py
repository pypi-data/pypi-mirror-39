from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Slider
from math import ceil

def version():
    return 5.3

class CapacityGraph:
    def __init__(self, infra):
        self._infra = infra
        self._fig = plt.figure()
        self._fig.suptitle("Used Search Capacity vs QPS")

    def _set_qps_list(self, qps_list):
        self._qps_values = [t[0] for t in qps_list]
        self._qps_labels = [t[1] for t in qps_list]

    def _search_budget_fix_pt(self, qps_list, pt):
        return [self._infra.get_used_search_capacity(qps, pt) for qps in qps_list]

    def plot(self, ax, qps_list, pt):
        self._set_qps_list(qps_list)
        capacity = self._search_budget_fix_pt(self._qps_values, pt)
        ax.plot(range(len(self._qps_values)), capacity, label="CPU Budget")
        ax.set_xticklabels(self._qps_labels)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
        ax.axhline(1, color="r", ls="--")
        ax.annotate(
            "Cluster max capacity",
            xy=(0, 1),
            verticalalignment="center",
            backgroundcolor="w",
        )
        for dsn in range(1, self._dsns + 1):
            lpos = 1 + dsn / 3
            ax.axhline(lpos, color="g", ls="--")
            ax.annotate(
                "DSN {}".format(dsn),
                xy=(0, lpos),
                verticalalignment="center",
                backgroundcolor="w",
            )
        ax.legend()


class CapacityGraphInteractive(CapacityGraph):
    def __init__(self, infra, pt_list, dsns):
        super().__init__(infra)
        self._dsns = dsns
        self._fig.subplots_adjust(bottom=0.23)
        self._ax = self._fig.subplots()
        self._make_slider(pt_list[0], pt_list[1])

    def _make_slider(self, min_pt, max_pt):
        axpt = plt.axes([0.27, 0.075, 0.50, 0.05])
        self._pt = (min_pt + max_pt) / 2
        self._slider_pt = Slider(axpt, "PT", min_pt, max_pt, valinit=self._pt)
        self._slider_pt.on_changed(self._update)

    def _update(self, val):
        self._pt = self._slider_pt.val
        self._ax.get_lines()[0].set_ydata(
            self._search_budget_fix_pt(self._qps_values, self._pt)
        )
        self._fig.canvas.draw_idle()

    def plot(self, qps_list):
        self._qps_list = qps_list
        super().plot(self._ax, self._qps_list, self._pt)
        plt.show()


class CapacityGraphGrid(CapacityGraph):
    def __init__(self, infra, pt_list, dsns):
        len_pt = len(pt_list)
        if len_pt == 0:
            raise ValueError("pt_list should have at least 1 element")

        super().__init__(infra)
        self._dsns = dsns
        self._pt_list = pt_list
        self._gs = gridspec.GridSpec(
            ceil(len_pt / 2), 1 if len_pt < 2 else 2, wspace=0.3, hspace=0.4
        )

    def plot(self, qps_list):
        for i, pt in enumerate(self._pt_list):
            ax = self._fig.add_subplot(self._gs[i])
            super().plot(ax, qps_list, pt)
            ax.set_title("PT = {}".format(pt))
        plt.show()
