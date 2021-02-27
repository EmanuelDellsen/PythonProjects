import matplotlib.pyplot as plt
import numpy as np
import matplotlib.axes as axes
from math import log
import csv

chalmers_csv_list = []
grp_10_list = []

csvReader = csv.reader(open('GroundSteeringRequest-0.csv'), delimiter=";")
for row in csvReader:
    chalmers_csv_list.append(row) 

csvReader = csv.reader(open("SRV_group_10_4_may.csv"), delimiter=",")
for row in csvReader:
    grp_10_list.append(row)

# remove title of first column in chalmers csv
chalmers_csv_list.pop(0)

# remove title of first column in group_10 csv
grp_10_list.pop(0)

# store timestamp from group_10 csv in variable
TS_grp_10 = [i[0] for i in grp_10_list]
TS_grp_10_floats = []
# iterate over the list of timestamps to cast them to float in order to
# enable plotting of the values on the graph
for item in TS_grp_10: 
    try: 
        float(item)
        item = float(item)
        item = item/1000000
        TS_grp_10_floats.append(item)
    except ValueError: 
        print(item)    
        
# store groundsteering request from group_10 csv in variable
GSR_grp_10 = [i[1] for i in grp_10_list]

print(GSR_grp_10[0])
GSR_grp_10_floats = []

# iterate over the list of groundsteering requests to cast them to float 
# in order to enable plotting of the values on the graph
for item in GSR_grp_10: 
    try: 
        float(item)
        item = float(item)
        GSR_grp_10_floats.append(item)
    except ValueError: 
        print(item)

gsr_len = len(GSR_grp_10_floats)

ts_len = len(TS_grp_10_floats)
print(gsr_len)
print(ts_len)
#print(GSR_grp_10_floats)
print(TS_grp_10_floats)
print(TS_grp_10_floats[0])

print(TS_grp_10_floats[ts_len-1])
print(GSR_grp_10_floats[0])
print(GSR_grp_10_floats[gsr_len-1])


print(GSR_grp_10_floats[gsr_len-1] + 0.28)
print("---------------------------------------------------------------------")

#ground steering request
GSR = [i[6] for i in chalmers_csv_list]
#sample timesamp seconds 
STSS = [i[4] for i in chalmers_csv_list]
#sample timestamp microseconds
STSMS = [i[5] for i in chalmers_csv_list]
for index, item in enumerate(GSR):
    GSR[index] = float(item)

array_len = len(STSS)

complete_arr = chalmers_csv_list

for i in range(array_len):
    microsec = STSMS[i]
    sec = STSS[i]
    merged = sec + '.'+ microsec
    complete_arr[i] = float(merged)

left = complete_arr[0]
right = complete_arr[array_len-1]



value = complete_arr[array_len-1] - complete_arr[0]
print(value)
plt.plot(complete_arr, GSR, 'r', label="Chalmers algorithm", linewidth=1)
plt.plot(TS_grp_10_floats, GSR_grp_10_floats, 'k', color='0.75', label="Group 10 algorithm", linewidth=1)
#plt.xticks(np.arange(TS_grp_10_floats[0], TS_grp_10_floats[ts_len-1] +1))

plt.ylabel('GroundSteeringRequest')
plt.xlabel('timestamp')
legend = plt.legend()


#plt.text(complete_arr[int(array_len/2)],GSR[int(array_len/2)], "Emanuel Dellsén", fontsize=12)
plt.show()

fig = plt.figure()
fig.savefig('GroundSteeringRequest.png', dpi=fig.dpi)
