# biodigestor -> biogas_in = waste_in[t]*efficiency
# tank  -> SOC(t+1) = SOC(t) + biogas_in - biogas_out
# biogas_out = ????
# tank cost = spec_cost * tank_size
# SOC <= tank_size 
# waste_in/day <= waste cap 
# waste_in(t) <= waste availability
# biodigestor_cost = waste_cap*spec_cost


#marti hai ragione! 
import numpy as np
import pandas as pd

kgs = 100             #chilos fed per day
kgs_season = 10000     #chilos fed per day
time_frame = [15,18]  #time of feeding of the biodigestor
time_step = 7         #in days
seasons = [90,120,270,300]          #in days

hours = np.zeros(8760)

for i in range(0,8760):
    day = int(np.floor(i/24))
    if i%24 >= time_frame[0] and i%24 <= time_frame[1] and day%time_step == 0:
        hours[i] = kgs/(time_frame[1]-time_frame[0])
        for j in range(0,(len(seasons)-1)):
            if (i%24 >= seasons[j] and i%24 <= seasons[j+1]):
                hours[i] += kgs_season/(time_frame[1]-time_frame[0])

series_frame = pd.DataFrame(hours)
series_frame.to_csv("Wastesupply.csv")
