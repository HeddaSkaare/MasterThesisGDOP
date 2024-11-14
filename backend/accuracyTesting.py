


from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from computebaner import get_gnss, getDayNumber
from satellitePositions import get_satellite_positions

#the mse function
def MSE(positions_old, positions_new):
    
    #calculate the difference between the two dataframes
    positions = pd.merge(positions_old, positions_new, on = "satelite_id", suffixes = ("_old", "_new"))

    positions["X_diff"] = positions["X_old"] - positions["X_new"]
    positions["Y_diff"] = positions["Y_old"] - positions["Y_new"]
    positions["Z_diff"] = positions["Z_old"] - positions["Z_new"]
    positions["distance"] = np.sqrt(positions["X_diff"]**2 + positions["Y_diff"]**2 + positions["Z_diff"]**2)
    #calculate the average accuracy
    averageAccuracy = positions["distance"].mean() *10e-6 #convert to km
    return averageAccuracy

#positions based on first date
def accuracyDataAll(gnss_list, startTime, endTime, timeDelta):

    daynumber = getDayNumber(startTime)#4. november
    gnss_mapping_old = get_gnss(daynumber)

    #sjekker hver 4 time
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).total_seconds() /3600
    iterations = int(hours_between_sart_and_end/timeDelta)

    accuracy_dict_time = {}
    for i in range(iterations+1):
       
        time = pd.to_datetime(startTime)+ pd.Timedelta(hours= i*timeDelta)

        time_str = time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        daynumber2 = getDayNumber(time_str)
        gnss_mapping_new = get_gnss(daynumber2)
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        accuracy_dict = {key: [] for key in gnss_list}
        for gnss in gnss_list:
            positions_old = get_satellite_positions(gnss_mapping_old[gnss],gnss,time)
            positions_new = get_satellite_positions(gnss_mapping_new[gnss],gnss,time)

            if not (positions_new.empty or positions_old.empty):
                averageMSE = MSE(positions_old, positions_new)
                accuracy_dict[gnss].append(averageMSE)

        accuracy_dict_time[time_str] = accuracy_dict

    return accuracy_dict_time

def accuracyDataOne(gnss,satelite_id, startTime, endTime, timeDelta):
    daynumber = getDayNumber(startTime)#4. november
    gnss_mapping_old = get_gnss(daynumber)

    #sjekker hver 4 time
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).total_seconds()/3600
    iterations = int(hours_between_sart_and_end/timeDelta)
 
    accuracy_time = []
    accuracy_list = []
    for i in range(iterations+1):
        time = pd.to_datetime(startTime)+ pd.Timedelta(hours= i*timeDelta)
        time_str = time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        daynumber2 = getDayNumber(time_str)
        gnss_mapping_new = get_gnss(daynumber2)
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        
        if satelite_id != '':
            dataframe_gnss_old = gnss_mapping_old[gnss]
            dataframe_gnss_new = gnss_mapping_new[gnss]

            dataframe_satellite_old =dataframe_gnss_old.loc[dataframe_gnss_old['satelite_id'] == satelite_id]
            dataframe_satellite_new =dataframe_gnss_new.loc[dataframe_gnss_new['satelite_id'] == satelite_id]
            
            positions_old = get_satellite_positions(dataframe_satellite_old,gnss,time)
            positions_new = get_satellite_positions(dataframe_satellite_new,gnss,time)

            if not (positions_new.empty or positions_old.empty):
                averageMSE = MSE(positions_old, positions_new)
                accuracy_list.append(averageMSE)
                accuracy_time.append(time_str[8:10] + '/' + time_str[5:7] + ' ' + time_str[11:13])

        

    return accuracy_time, accuracy_list

#find mse for all calculations
gnssList = ['GLONASS', 'GPS', 'Galileo', 'BeiDou', 'QZSS']
gnss = 'GPS'
satelite_id = 'G02'
all = accuracyDataAll(gnssList, '2024-11-04T12:00:00.000', '2024-11-08T12:00:00.000', 6)

#times, acurracys = accuracyDataOne(gnss, satelite_id, '2024-11-04T12:00:00.000', '2024-11-08T12:00:00.000', 4)

def plotMultiple(gnss_list, accuracy_dict_time):
    timeList = []
    gnssList = []
    
    for gnss in gnss_list:
        gnssList.append([])
    
    for key in accuracy_dict_time:
        set = True
        values = accuracy_dict_time[key]
        i = 0
        for gnss in gnss_list:
            if values[gnss] == []:
                  set = False
        if set:
            for gnss in gnss_list:
                gnssList[i].append(values[gnss])
                i+=1
            timeList.append(key[8:10] + '/' + key[5:7] + ' ' + key[11:13])

    j = 0
    plt.figure(figsize=(12, 6))
    for gnss in gnss_list:
        plt.plot(timeList, gnssList[j], label = gnss ,linewidth=2, marker='o')
        j+=1
    
    plt.grid(visible=True, linestyle='--', alpha=0.6)
    # Add labels and title
    plt.title("GNSS Data Over Time", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("MSE (km^2)", fontsize=14)
    plt.legend(title="GNSS", fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

def plotOne(times, acurracys, gnss, satelite_id):

    plt.figure(figsize=(12, 6))
    
    plt.plot(times, acurracys, label = gnss ,linewidth=2, marker='o')

    plt.grid(visible=True, linestyle='--', alpha=0.6)
    # Add labels and title
    plt.title("MSE over time", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("MSE (km^2)", fontsize=14)
    plt.legend(title=satelite_id, fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

plotMultiple(gnssList, all)
#plotOne(times, acurracys, gnss, satelite_id)