from pathlib import Path
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.figure as figure
import matplotlib.ticker as ticker

## CLASSES ##
class ExpGroupInfo:
    def __init__(self, trap_distr:str, e_sigma:float, e_mid:float):
        self.trap_distr: str = trap_distr
        self.Es: float = e_sigma
        self.Em: float = e_mid
    def __eq__(self, other):
        if type(other) == ExpGroupInfo:
            return (self.trap_distr == other.trap_distr
                    and self.Es == other.Es
                    and self.Em == other.Em)
        else: return False
    def initialize(self)->None:
        self.trap_distr= None
        self.Es= None
        self.Em= None
        return None
class Exp:
    def __init__(self, trap_distr:str, e_sigma:float, e_mid:float, v_gf:int, file_path:Path):
        self.groupInfo: ExpGroupInfo = ExpGroupInfo(trap_distr, e_sigma, e_mid)
        self.Vgf: int = v_gf
        self.path:Path = file_path
class ExpGroup:
    def __init__(self, trap_distr:str, e_sigma:float, e_mid:float):
        self.info: ExpGroupInfo = ExpGroupInfo(trap_distr, e_sigma, e_mid)
        self.files:dict = {}    #{Vgf:file_path}
    def __contains__(self, item:Exp)->bool:
        return self.info == item.groupInfo
    def import_exp(self, item:Exp):
        self.files[item.Vgf] = item.path
        return None
class Curve:
    def __init__(self, name:str, vgf:int):
        self.name:str = name
        self.vgf:int = vgf
        self.X:np.ndarray = None
        self.Y:np.ndarray = None
    def sort(self)->None:
        i_sorted = np.argsort(self.X)
        self.X = self.X[i_sorted]
        self.Y = self.Y[i_sorted]
        return None
    def y_limits(self)->list:
        return self.Y.min(), self.Y.max()
class Plot:
    def __init__(self):
        self.fig: figure.Figure = None
        self.ax: axes.Axes = None
    def initialize(self)->None:
        self.fig, self.ax = plt.subplots(facecolor=Config.bk_color)
        self.ax.set_facecolor(Config.bk_color)
        return self
    def add_plot(self, curve:Curve)->None:
        self.ax.plot(curve.X, curve.Y,
                     label=curve.name if not Config.same_fig else curve.name+f"Vgf:{curve.vgf}",
                     color=CP.colors[curve.name] if Config.colors else 'black',
                     linestyle=None if Config.colors else CP.linestyles[curve.name],
                     marker=markers[curve.vgf] if Config.same_fig else 's',
                     linewidth=0.75 if Config.same_fig else None,
                     markersize=10 if markers[curve.vgf]=='*' and Config.same_fig else None)
        return None
    def graphics(self)->None:
        set_label(self.ax)
        spine_modifier(self.ax)
        ticks_modifier(self.ax)
        self.ax.grid(True, which='major', color=Config.sec_color, linestyle='-.', linewidth=0.5, alpha=0.6)
        if Config.legend:
            if not Config.same_fig:
                self.ax.legend(loc='best')
            else:
                custom_legend = [
                    # color legend
                    *(Line2D([], [], color=CP.colors[curve] if Config.colors else 'black', marker='o',
                             linestyle=None if Config.colors else CP.linestyles[curve], label=CP.names[curve])
                      for curve in CP.names),
                ]
                color_legend = self.ax.legend(
                    handles=custom_legend,
                    bbox_to_anchor=(0.5, -0.15),
                    loc="upper center",
                    ncol=len(CP.colors),
                    frameon=False,
                    fontsize=8,
                    handletextpad=0.5
                )
                custom_legend = [
                    # marker legend
                    *(Line2D([], [], color='black', marker=markers[Vgf], linestyle=None, label=f"Vgf={Vgf}",
                             markersize=10 if markers[Vgf] == '*' else None)
                      for Vgf in markers)
                ]
                self.ax.add_artist(color_legend)
                self.ax.legend(
                    handles=custom_legend,
                    bbox_to_anchor=(0.5, -0.22),
                    loc="upper center",
                    ncol=len(markers),
                    frameon=False,
                    fontsize=8,
                    columnspacing=1
                )
                # plt.tight_layout(rect=[0, 0.35, 1, 0.95])  # Leave 35% of lower space for the legends
        return None
    def save_fig(self, path:Path)->None:
        plt.figure(self.fig)
        plt.sca(self.ax)
        plt.savefig(path,
                    dpi=Config.DPI,
                    format=Config.ext,
                    bbox_inches='tight')
        return None
    def close(self)->None:
        plt.close(self.fig)
        return None
class CurvesExpSubGroup:
    def __init__(self, vgf:int):
        self.Vgf:int = vgf
        self.cv0:Curve = Curve('v0',vgf)
        self.c0:Curve = Curve('0',vgf)
        self.c15:Curve = Curve('15',vgf)
        self.c30:Curve = Curve('30',vgf)
    def sort(self)-> None:
        self.cv0.sort()
        self.c0.sort()
        self.c15.sort()
        self.c30.sort()
        return None
    def import_csv(self, path:Path)->None:
        if not path.exists():
            raise FileNotFoundError(f"File {path} non trovato!")
        try:
            data = pd.read_csv(path)
            data.replace('-', '0', inplace=True)
                # export of the dataframe data to the cache
            for col in data.columns:
                sel = np.array(col.split(' '), dtype=str)  # [curve_name X/Y]
                for name, curve in vars(self).items():
                    if type(curve) is Curve:
                        if curve.name == sel[0]:
                            match sel[1]:
                                case 'X': curve.X = data[col].to_numpy(dtype=float)
                                case 'Y': curve.Y = data[col].to_numpy(dtype=float)
            self.sort()
        except Exception as e:
            print(f"Errore leggendo {path}: {e}")
            raise
        return None
    def y_limits_group(self)->list:
        cv0_min, cv0_max = self.cv0.y_limits()
        c0_min, c0_max = self.c0.y_limits()
        c15_min, c15_max = self.c15.y_limits()
        c30_min, c30_max = self.c30.y_limits()
        return min(cv0_min, c0_min, c15_min, c30_min), max(cv0_max, c0_max, c15_max, c30_max)
    def plot_all(self)->Plot:
        plot = Plot()
        plot.initialize()
        for name, curve in vars(self).items():
            if type(curve) is Curve:
                plot.add_plot(curve)
        return plot
class PlotExpGroup:
    def __init__(self):
        self.info:ExpGroupInfo = ExpGroupInfo(None,None,None)
        self.main:Plot = Plot()
        self.plots:dict[int,Plot] = {}
    def initialize(self)->None:
        self.info.initialize()
        self.main.initialize()
        for Vgf in self.plots:
            self.plots[Vgf].initialize()
        return None
    def close(self)->None:
        self.main.close()
        for Vgf in self.plots:
            self.plots[Vgf].close()
        self.plots.clear()
        return None

## PARAMS ##
class Config:
    DPI = 300
    bk_color = 'white'
    ext = 'png'  # png,svg,pdf
    sort_output = True
    same_fig_choice = 'both'  # yes,no,both
    same_fig = True if same_fig_choice in ('yes', 'both') else False
    same_y_scale = True
    legend = True
    colors = True

    # automatic derived params
    if same_fig: same_y_scale = True
    sec_color = 'black' if bk_color == 'white' else 'white'
class CP:   # curves params
    names = {
        "v0": "(0,0)",
        "0": "(-7,0)",
        "15": "(-7,15)",
        "30": "(-7,30)"
    }
    colors = {
        "v0": "red",
        "0": "limegreen",
        "15": "dodgerblue",
        "30": "darkorange"
    }
    linestyles = {
        "v0": "dashdot",
        "0": "dotted",
        "15": "dashed",
        "30": "solid"
    }   # to use in case of colorless image configuration
markers = {
    -2: "s",
    -1: "o",
    0: "v",
    1: "d",
    2: "*"
}  # to use in same fig, multiple plots

## FUNCTIONS ##
def set_label(ax:"axes.Axes")->None:
    # axis labels
    ax.set_xlabel(r'$V_d \, _{[V]}$', fontsize=20, color=Config.sec_color)  # x-label
    ax.set_ylabel(r'$I_d \, _{[A/mm]}$', fontsize=20, color=Config.sec_color)  # y-label
def spine_modifier(ax:"axes.Axes")->None:
    for name, spine in ax.spines.items():
        if name=='right'or name=='top':
            spine.set_visible(False)
        else:
            spine.set_color(Config.sec_color)
def ticks_modifier(ax:"axes.Axes")->None:
    #   x-axis
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    #   y-axis
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.04))

    # set a label void every couple
    x_ticks_pos = ax.get_xticks()
    x_labels = [label.get_text() if i % 2 == 0 else '' for i, label in enumerate(ax.get_xticklabels())]
    ax.set_xticks(x_ticks_pos,labels=x_labels)

    ax.tick_params(axis='both', which='both', colors=Config.sec_color)