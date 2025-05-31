from Common import Config as cfg

## FUNCTIONS ##
def represents_int(s):
    try: int(s)
    except ValueError: return False
    else: return True
def input_bool(var_name:str,var:bool)->bool:
    while True:
        match input(f"\t{var_name}: {var} -> "):
            case "True"|"true"|"T"|"t": return True
            case "False"|"false"|"F"|"f": return False
            case "": return var

## MAIN ##
def main()->None:
    print(f"\tTRAP DISTRIBUTION PLOTTER\n"
          f"\nParametri di funzionamento principali: "
          f"\n\t·background color (default {cfg.bk_color})"
          f"\n\t·stessa scala nei due assi y (default {cfg.same_y_scale})"
          f"\n\t·legenda presente (default {cfg.legend})"
          # f"\n\t·figura di output a colori (default {cfg.colors})"
          f"\n\t·output extension (default {cfg.ext})"
          f"\n\t·output file DPI (default {cfg.DPI})"
          f"\n\t·sorting dell'output in cartelle (default {cfg.sort_output})"
          f"\nDesideri cambiarne uno? [yes/no]")
    while True:
        match input("\t"):
            case "yes"|"y":
                print("Inserisci i nuovi valori (Invio per non modificare)")

                while True:
                    choice=input(f"\tbk_color: {cfg.bk_color} -> ")
                    if choice in ("black","white"):
                        cfg.bk_color=choice
                        break
                    elif choice == "": break

                cfg.same_y_scale = input_bool("same_y_scale",cfg.same_y_scale)
                cfg.legend = input_bool("legend",cfg.legend)
                # cfg.colors = input_bool("colors",cfg.colors)

                while True:
                    choice=input(f"\toutput_ext: {cfg.ext} -> ")
                    if choice in ('png','svg','pdf'):
                        cfg.ext=choice
                        break
                    elif choice == '': break

                while True:
                    choice=input(f"\toutput_DPI: {cfg.DPI} -> ")
                    if represents_int(choice):
                        if int(choice)>0:
                            cfg.DPI=int(choice)
                            break
                    elif choice == '': break

                cfg.sort_output = input_bool("output_sort",cfg.sort_output)
            case "no"|"n":
                return None
        print("desideri fare altri cambiamenti? [yes/no]")
