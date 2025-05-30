from Common import *
from Common import Config as cfg

## CACHE MEM ##
group_to_plot:ExpGroup # contains paths to csv files of group curves
Out = PlotExpGroup()

## MAIN ##
def main()->None:
    global Out
    Out.info = group_to_plot.info

    # params
    y_min, y_max = 0,1
    # cache
    group_list:list[CurvesExpSubGroup] = []

    # DATA EXTRACTION
    for Vgf in group_to_plot.files:
        temp = CurvesExpSubGroup(Vgf)
        if group_to_plot.files[Vgf] is not None:
            temp.import_csv(group_to_plot.files[Vgf])
            yMin,yMax = temp.y_limits_group()   # subGroup y limits
            y_min,y_max = min(y_min, yMin),max(y_max, yMax)
            group_list.append(temp) # copying the curves values in the main dict at their Vgf
        else:
            print(f"\t! No data for Vgf={Vgf} !")   # if there's no data for the respective Vgf

    # PLOTS CREATION
    if cfg.same_fig:    # creating a plot for the entire group
        Out.main.initialize()
        for subGroup in group_list:
            for name, curve in vars(subGroup).items():
                if type(curve) is Curve:
                    Out.main.add_plot(curve)
    else:   # creating a plot for every group element
        for subGroup in group_list:
            temp = subGroup.plot_all()
            if cfg.same_y_scale:    # same scaling of the y axes (if settled so)
                y_tolerance = (y_max - y_min) / 20
                temp.ax.set_ylim(y_min - y_tolerance, y_max + y_tolerance)
            Out.plots[subGroup.Vgf] = temp

    # GRAPHICS
    if cfg.same_fig:
        Out.main.graphics()
    else:
        for subGroupPlot in Out.plots.values():
            subGroupPlot.graphics()

    return None