DPI = 300
bk_color = 'white'
ext = 'png' # png,svg,pdf
sort_output = True
same_fig_choice = 'both' # yes,no,both
same_fig = True if same_fig_choice in ('yes','both') else False
same_y_scale = True
legend = True
colors = True

# automatic derived params
if same_fig: same_y_scale = True