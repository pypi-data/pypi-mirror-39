from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Slider
from math import ceil


def _search_budget_fix_pt(infra, qps, pt):
    return [infra.get_used_search_capacity(q, pt) for q in qps]


def capacity_graph(infra, qps_list, proc_times):
    capacity = _search_budget_fix_pt(infra, qps_list, 10)
    fig = plt.figure(constrained_layout=True)
    fig.suptitle("Capacity graph")
    ax = fig.subplots()
    l, = plt.plot(qps_list, capacity, label="CPU Budget")
    plt.axhline(1, color="r", ls="--", label="Max CPU budget")

    # Format
    plt.legend()
    ax.set_xlabel("QPS")
    ax.set_ylabel("Used Search Capacity")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
    axpt = plt.axes(
        [0.27, 0.075, 0.50, 0.05]
    )  # Create a new axes (container for axis to be used for the slider)
    slider_pt = Slider(axpt, "PT", 5, 20, valinit=15)

    def update(val):
        pt = slider_pt.val
        print(pt)
        # update curve
        l.set_ydata(_search_budget_fix_pt(infra, qps_list, pt))
        # redraw canvas while idle
        fig.canvas.draw_idle()

    slider_pt.on_changed(update)
    fig.set_constrained_layout({"w_pad": 0.7, "h_pad": 0.7})

    plt.show()


def _plot_capacity(ax, infra, qps_list, pt):
    capacity = _search_budget_fix_pt(infra, qps_list, pt)
    ax.plot(qps_list, capacity, label="CPU Budget")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.0%}".format(y)))
    ax.set_title("PT = {}".format(pt))
    ax.axhline(1, color="r", ls="--", label="Max CPU budget")
    ax.legend()


def capacity_graph_grid(infra, qps_list, proc_times):
    len_pts = len(proc_times)
    if len_pts == 0:
        raise ValueError("proc_times should have at least 1 element")
    if len_pts >= 6:
        raise ValueError("proc_times should be smaller than 6")

    fig = plt.figure()
    fig.suptitle("Used Search Capacity vs QPS graph")
    if len_pts == 1:
        ax = fig.subplots()
        _plot_capacity(ax, infra, qps_list, proc_times[0])
    else:
        axes = fig.subplots(ceil(len_pts / 2), 2)
        flat_axes = [ax for sublist in axes for ax in sublist]
        for i, pt in enumerate(proc_times):
            _plot_capacity(flat_axes[i], infra, qps_list, pt)
        if len_pts % 2 != 0:
            flat_axes[-1].axis('off')

    plt.tight_layout(pad=2)
    plt.show()
