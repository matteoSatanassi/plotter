import config_manager
import file_manager
import time

config_manager.main()
start_time = time.time()
n_plots = file_manager.main()
end_time = time.time()
print(f"\n{n_plots} grafici creati"
      f"\nTempo di esecuzione: {end_time-start_time}s")