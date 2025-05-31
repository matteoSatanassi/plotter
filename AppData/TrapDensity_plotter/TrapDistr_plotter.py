from Common import*
from Common import Config as cfg

    # CACHE MEM
curves_to_plot = ExpCurves(None)
Out = Plot()

## MAIN ##
def main()->None:
    global Out
    Out.initialize()

    # DATA EXTRACTION
    curves_to_plot.data_extraction()

    # PLOT CREATION
    Out.add_curve(curves_to_plot.td)
    for key,curve in curves_to_plot.ctd.items():
        Out.add_curve(curve)

    # same scaling of the y axes (if settled so)
    if cfg.same_y_scale:
        Out.set_same_scale(curves_to_plot)

    # Graphics
    Out.graphics()

    return None