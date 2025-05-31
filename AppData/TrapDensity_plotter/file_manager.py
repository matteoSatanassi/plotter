from Common import *
from Common import Config as cfg
import TrapDistr_plotter as plotter

## PARAMS ##
script_dir = Path(__file__).parent.absolute()   # Get the current working directory
base_dir = script_dir.parent.parent   # Get the parent directory
data_dir = base_dir/'TrapDistr'/'data'
to_save_dir = base_dir/'TrapDistr'/'output'

## FUNCTIONS ##
def find_dir(file:str)->Path:
        #cache mem
    info=np.array(file.split('_')) #es: TrapData_exponential_Vgf_2_Es_1.72_Em_1.04_(0,0)
    curr_file = ExpGroupInfo(info[3],info[5],info[7])

    output_dir= to_save_dir/f"Es_{curr_file.Es}"/f"Em_{curr_file.Em}"/f"Vgf_{curr_file.Vgf}"
    try:
        output_dir.mkdir(parents=True)
        print(f" Created directory: {output_dir}")
    except FileExistsError:
        pass

    return output_dir

## MAIN ##
def main()->int:
    output_dir = to_save_dir

    print("\nSTARTING PROCESS...")
    file_list = list(Path(data_dir).glob('*.csv'))   #list of all .csv files in data directory

    for file in file_list:
        print(f"\nProcessing {file.name}")
        plotter.curves_to_plot.path = file
        plotter.main()
        print(" -> plotting done")
        if cfg.sort_output:
            output_dir=find_dir(file.stem)
        plotter.Out.save_fig(output_dir / f"{file.stem}.{cfg.ext}")
        print(f" -> file saved in {output_dir}")
        plotter.Out.close()

    print("\nPROCESS FINISHED...")
    return len(file_list)