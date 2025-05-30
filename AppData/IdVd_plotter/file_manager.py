from Common import *
from Common import Config as cfg
import IdVd_plotter as plotter

## PARAMS ##
script_dir = Path(__file__).parent.absolute()   # Get the script directory
base_dir = script_dir.parent.parent   # Get the parent directory
data_dir = base_dir/'IdVd'/'data'
output_dir = base_dir/'IdVd'/'output'

## CACHE MEM ##
n_plots:int

## FUNCTIONS ##
def try_mkdir(path)->None:
    try:
        path.mkdir(parents=True)
        print(f" Created directory: {path}")
    except FileExistsError:
        pass
    return None
def info_extract(file_path:Path)->Exp:
    info = np.array((file_path.stem.split('_'))) #es: IdVd_exponential_Vgf_2_Es_1.72_Em_1.04
    out = Exp(
        trap_distr=info[1],
        e_sigma=float(info[5]),
        e_mid=float(info[7]),
        v_gf=int(info[3]),
        file_path=file_path
    )
    return out
def save()->None:   # takes plotter.Out and saves every figure
    global n_plots
    # defining saving directory, default output_dir
    toSave_dir = output_dir

    print(" saving plots")
    out_file_name = f"IdVd_{plotter.Out.info.trap_distr}_Es_{plotter.Out.info.Es}_Em_{plotter.Out.info.Em}"
    if cfg.same_fig_choice in ('yes','both'):
        if cfg.sort_output: # toSave_dir elaboration if sort_output=True
            toSave_dir = output_dir / f'Es_{plotter.Out.info.Es}'
            try_mkdir(toSave_dir)
        plotter.Out.main.save_fig(toSave_dir / f"{out_file_name}.{cfg.ext}")
        print(f" -> file {out_file_name}.{cfg.ext} saved in {toSave_dir}")
        n_plots += 1
    if cfg.same_fig_choice in ('no','both'):
        if cfg.sort_output:
            toSave_dir = output_dir / f'Es_{plotter.Out.info.Es}' / f'Em_{plotter.Out.info.Em}'
        try_mkdir(toSave_dir)
        for Vgf in plotter.Out.plots:
            plotter.Out.plots[Vgf].save_fig(toSave_dir / f"{out_file_name}_Vgf_{Vgf}.{cfg.ext}")
            print(f" -> file {out_file_name}_Vgf_{Vgf}.{cfg.ext} saved in {toSave_dir}")
            n_plots += 1

    return None

## MAIN ##
def main()->int:
    global n_plots
    n_plots = 0

    print("\nSTARTING PROCESS...")
    file_list = list(Path(data_dir).glob('*.csv'))   #list of all .csv files path in data directory
    
    print("\n files preprocess...")
    # cache mem
    Groups:list[ExpGroup] = []

    # data extraction and Groups list filler
    for file in file_list:
        temp = info_extract(file)
        group = next((g for g in Groups if temp in g),None)
        if group is None:
            group = ExpGroup(
                trap_distr=temp.groupInfo.trap_distr,
                e_sigma=temp.groupInfo.Es,
                e_mid=temp.groupInfo.Em
            )
            Groups.append(group)
        group.import_exp(temp)

    print(" -> preprocess finished")

    for group in Groups:
        plotter.group_to_plot = group   # saving current group in plotter cache
        plotter.Out.initialize()    # emptying plotter.Out

        print(f'\nProcessing group: {group.info.trap_distr},Es: {group.info.Es},Em: {group.info.Em}')
        if cfg.same_fig_choice == 'both':
            cfg.same_fig = True
            print(" plotting group in same figure")
            plotter.main()
            print(" -> plotting done")
            cfg.same_fig = not cfg.same_fig # changing app config
            print(" plotting group's curves")
        plotter.main()
        print(" -> plotting done")

        save()  # saving plots contained in plotter.Out
        plotter.Out.close() # closing open figures

    print("\nPROCESS FINISHED...")

    return n_plots