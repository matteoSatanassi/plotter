from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib.axes as axes
import matplotlib.ticker as ticker

## CLASSES ##
class ColInfo:
    def __init__(self):
        self.col:str = None
        self.pos:float = None
        self.cord:str = None
    def read(self, col:str):
        self.col = col
        temp = col.split(" ")
        self.cord = temp[1]
        for word in temp[0].split("_"):
            try:
                self.pos = float(word)
            except ValueError:
                pass
        return self
class ExpGroupInfo:
    def __init__(self, vgf:str, e_sigma:str, e_mid:str):
        self.Vgf:str = vgf
        self.Es:str = e_sigma
        self.Em:str = e_mid
class Curve:
    def __init__(self, pos:float=None):
        self.pos:float = pos
        self.X:np.ndarray = None
        self.Y:np.ndarray = None
    def sort(self)->None:
        i_sorted = np.argsort(self.X)
        self.X = self.X[i_sorted]
        self.Y = self.Y[i_sorted]
        return None
    def y_limits(self)->list[float]:
        return self.Y.min(), self.Y.max()
class ExpCurves:
    def __init__(self, path:Path):
        self.path:Path = path
        self.td = Curve()
        self.ctd:dict[float,Curve] = {}
    def sort(self)->None:
        self.td.sort()
        for key,curve in self.ctd.items():
            curve.sort()
    def data_extraction(self)->None:
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} non trovato!")
        try:
            data = pd.read_csv(self.path)
            data.replace('-', '0', inplace=True)
            for col in data.columns:
                col_info = ColInfo().read(col)
                if "trap_density" in col_info.col:
                    right_curve =self.td
                else:
                    if col_info.pos not in self.ctd:
                        self.ctd[col_info.pos] = Curve(col_info.pos)
                    right_curve = self.ctd[col_info.pos]
                if col_info.cord == "X":
                    right_curve.X = data[col].to_numpy(dtype=float)
                elif col_info.cord == "Y":
                    right_curve.Y = data[col].to_numpy(dtype=float)
                else:
                    raise KeyError(f"coordinata {col_info.cord} non trovata!")
            self.sort()
        except Exception as e:
            print(f"Errore leggendo {self.path}: {e}")
            raise
        return None
    def y_limits(self)->list[float]:
        MIN,MAX = 0,1
        min_c,max_c = self.td.y_limits()
        MIN, MAX = min(MIN, min_c), max(MAX, max_c)
        for curve in self.ctd.values():
            min_c,max_c = curve.y_limits()
            MIN,MAX = min(MIN,min_c),max(MAX,max_c)
        return MIN,MAX
class Plot:
    def __init__(self):
        self.fig: figure.Figure = None
        self.ax_td: axes.Axes = None
        self.ax_ctd: axes.Axes = None
    def initialize(self)->'Plot':
        self.fig, self.ax_ctd = plt.subplots(facecolor=Config.bk_color)
        self.ax_td = self.ax_ctd.twinx()

        self.ax_td.set_facecolor(Config.bk_color)
        self.ax_ctd.set_facecolor(Config.bk_color)
        return self
    def add_curve(self, curve:Curve)->None:
        if curve.pos is None:
            self.ax_td.plot(curve.X, curve.Y,
                            label="Trap Density",
                            color=CP.colors[curve.pos],
                            # color=CP.colors[curve.pos] if Config.colors else 'black',
                            # linestyle=None if Config.colors else CP.linestyles[curve.pos],
                            marker='o'
                            )
        else:
            self.ax_ctd.plot(curve.X, curve.Y,
                             label=f"x={curve.pos} [μm]",
                             color=CP.colors[curve.pos],
                             # color=CP.colors[curve.pos] if Config.colors else 'black',
                             # linestyle=None if Config.colors else CP.linestyles[curve.pos],
                             marker='s'
                            )
        return None
    def set_same_scale(self,curves:ExpCurves)->None:
        yMin,yMax = curves.y_limits()
        tolerance = (yMax - yMin)/20
        self.ax_td.set_ylim(yMin-tolerance,yMax+tolerance)
        self.ax_ctd.set_ylim(yMin-tolerance,yMax+tolerance)
        return None
    def graphics(self)->None:
        set_labels(self)
        spine_modifier(self)
        set_ticks(self)
        set_grid(self)
        if Config.legend:
            set_legend(self)
        return None
    def save_fig(self, path:Path)->None:
        self.fig.tight_layout()
        self.fig.savefig(path,
                    dpi=Config.DPI,
                    format=Config.ext,
                    bbox_inches='tight'
                    )
        return None
    def close(self)->None:
        if self.fig:
            plt.close(self.fig)
        self.fig,self.ax_ctd,self.ax_td = None,None,None
        return None

## PARAMS ##
class Config:
    bk_color = 'white'
    DPI = 300
    ext = 'png'
    # colors = True
    legend = True
    sort_output = True
    same_y_scale = True

    # derived params
    sec_color = 'black' if bk_color == 'white' else 'white'
class CP:   # curve params
    colors = {
        None: 'black',
        0.5000:"#1f77b4",  # blu
        0.6160:"#ff7f0e",  # arancione
        0.7660:"#2ca02c",  # verde
        0.7830:"#d62728",  # rosso
        0.9670:"#9467bd",  # viola
        0.9840:"#8c564b",  # marrone
        1.1840:"#e377c2",  # rosa
        1.3340:"#17becf",  # azzurro
        1.8340:"#bcbd22",  # giallo
    }
    # linestyles = {
    #     None: 'solid',
    #     0.5000: 'dotted',
    #     0.9500: 'dashed',
    #     0.9840: 'dashdot',
    #     1.1840: (0, (3, 1, 1, 1)),   #densely dashdotted
    #     1.3340: (0, (3, 5, 1, 5, 1, 5)), #dashdotdotted
    #     1.8340: (5, (10, 3)) #long dash with offset
    # }

## FUNCTIONS ##
def set_labels(plot:Plot)->None:
    plot.ax_ctd.set_xlabel(r'$E \, [eV]$', fontsize=15, color=Config.sec_color)  # x-label
    plot.ax_ctd.set_ylabel(r'$Charged\:Trap\:density \, _{[1/cm^3\!\cdot\!eV]}$', fontsize=15, color=Config.sec_color)  # y-label
    plot.ax_td.set_ylabel(r'$Trap\:density \, _{[1/cm^3\!\cdot\!eV]}$', fontsize=15, color=Config.sec_color)  # y-label
    return None
def spine_modifier(plot:Plot)->None:
    for name,spine in plot.ax_ctd.spines.items():
        if name == 'top': spine.set_visible(False)
        else: spine.set_color(Config.sec_color)
    return None
def set_ticks(plot:Plot)->None:
    #   x-axis
    plot.ax_ctd.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    plot.ax_ctd.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    #   left y-axis
    plot.ax_ctd.yaxis.set_major_locator(ticker.MultipleLocator(0.5e13))
    plot.ax_ctd.yaxis.set_minor_locator(ticker.MultipleLocator(0.1e13))
    #   right y-axis
    plot.ax_td.yaxis.set_major_locator(ticker.MultipleLocator(0.5e13))
    plot.ax_td.yaxis.set_minor_locator(ticker.MultipleLocator(0.1e13))
    #   setting ticks params
    plot.ax_ctd.tick_params(axis='both', which='both', colors=Config.sec_color)
    plot.ax_td.tick_params(axis='y', which='both', colors=Config.sec_color)
    return None
def set_grid(plot:Plot)->None:
    plot.ax_ctd.grid(True, which='major', color=Config.sec_color, linestyle='--', linewidth=0.5, alpha=0.6)
    plot.ax_ctd.grid(True, which='minor', color=Config.sec_color, linestyle='-.', linewidth=0.25, alpha=0.6)
    return None
def set_legend(plot:Plot)->None:
    plot.ax_td.legend(facecolor=Config.bk_color, edgecolor=Config.sec_color, labelcolor=Config.sec_color, loc='upper right')
    plot.ax_ctd.legend(facecolor=Config.bk_color, edgecolor=Config.sec_color, labelcolor=Config.sec_color, loc='upper left')

