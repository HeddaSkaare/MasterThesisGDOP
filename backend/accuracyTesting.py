


from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from computebaner import get_gnss, getDayNumber
from satellitePositions import get_satellite_positions



#the mse function
def MSE(positions_old, positions_new, notAcceptedSatellites):
    
    #calculate the difference between the two dataframes
    positions = pd.merge(positions_old, positions_new, on = "satelite_id", suffixes = ("_old", "_new"))
    positions = positions[~positions['satelite_id'].isin(notAcceptedSatellites)]
    positions["X_diff"] = (positions["X_old"] - positions["X_new"])
    positions["Y_diff"] = (positions["Y_old"] - positions["Y_new"])
    positions["Z_diff"] = (positions["Z_old"] - positions["Z_new"])
    positions["distance"] = np.sqrt(positions["X_diff"]**2 + positions["Y_diff"]**2 + positions["Z_diff"]**2)
    for index, row in positions.iterrows():
        if row["distance"] > 10000:
            print(row["satelite_id"], row["distance"])
    #calculate the average accuracy
    averageAccuracy = positions["distance"].median()  #convert to km
    return averageAccuracy

def position(positions_old, positions_new):
    
    #calculate the difference between the two dataframes
    
    positions_old["distanceOld"] = (np.sqrt(positions_old["X"]**2 + positions_old["Y"]**2 + positions_old["Z"]**2)* 10**(-3)) - 6378
    positions_new["distanceNew"] = (np.sqrt(positions_new["X"]**2 + positions_new["Y"]**2 + positions_new["Z"]**2)*10**(-3)) - 6378
    #calculate the average accuracy
    
    return positions_old["distanceOld"], positions_new["distanceNew"]

def positionXYZ(positions_old, positions_new):
    
    #calculate the difference between the two dataframes
    print(positions_old)
    positions_old["distanceBetween"] = (np.sqrt((positions_new["X"]-positions_old["X"])**2 + (positions_new["Y"]-positions_old["Y"])**2 + (positions_new["Z"]-positions_old["Z"])**2))
    positions_old["distanceX"] = (positions_new["X"]-positions_old["X"])
    positions_old["distanceY"] = (positions_new["Y"]-positions_old["Y"])
    positions_old["distanceZ"] = (positions_new["Z"]-positions_old["Z"]) 
    #calculate the average accuracy
    
    return positions_old["distanceBetween"] , positions_old["distanceX"], positions_old["distanceY"], positions_old["distanceZ"]

#positions based on first date
def accuracyDataAll(gnss_list,notAcceptedSatellites, startTime, endTime, timeDelta):

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

        daynum2_minus_1 = int(daynumber2)  - 1
        daynumber2_minus_1 = f"{daynum2_minus_1:03d}"
        gnss_mapping_new2 = get_gnss(daynumber2_minus_1)
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        accuracy_dict = {key: [] for key in gnss_list}
        for gnss in gnss_list:
            dataframe_satellite_new2 = gnss_mapping_new2[gnss]
       
            newDataframe = pd.concat([gnss_mapping_new[gnss], dataframe_satellite_new2])

            positions_old = get_satellite_positions(gnss_mapping_old[gnss],gnss,time)
            positions_new = get_satellite_positions(newDataframe,gnss,time)

            if not (positions_new.empty or positions_old.empty):
                averageMSE = MSE(positions_old, positions_new,notAcceptedSatellites)
                accuracy_dict[gnss].append(averageMSE)

        accuracy_dict_time[time_str] = accuracy_dict

    return accuracy_dict_time

def accuracyDataOne(gnss,satelite_id,notAcceptedSatellites, startTime, endTime, timeDelta):
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
        daynum2_minus_1 = int(daynumber2)  - 1
        daynumber2_minus_1 = f"{daynum2_minus_1:03d}"
        gnss_mapping_new2 = get_gnss(daynumber2_minus_1)
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        
        if satelite_id != '':
            dataframe_gnss_old = gnss_mapping_old[gnss]
            dataframe_gnss_new = gnss_mapping_new[gnss]
            dataframe_gnss_new2 = gnss_mapping_new2[gnss]

            dataframe_satellite_old =dataframe_gnss_old.loc[dataframe_gnss_old['satelite_id'] == satelite_id]
            dataframe_satellite_new =dataframe_gnss_new.loc[dataframe_gnss_new['satelite_id'] == satelite_id]
            dataframe_satellite_new2 =dataframe_gnss_new2.loc[dataframe_gnss_new2['satelite_id'] == satelite_id].tail(2)
            #adds the old dataframes to the new one
            dataframe_satellite_new = pd.concat([dataframe_satellite_new2,dataframe_satellite_new])

            positions_old = get_satellite_positions(dataframe_satellite_old,gnss,time)
            positions_new = get_satellite_positions(dataframe_satellite_new,gnss,time)

            if not (positions_new.empty or positions_old.empty):
                averageMSE = MSE(positions_old, positions_new,notAcceptedSatellites)
                accuracy_list.append(averageMSE)
                accuracy_time.append(time_str[8:10] + '/' + time_str[5:7] + ' ' + time_str[11:13])

        

    return accuracy_time, accuracy_list

def positionsDataOne(gnss,satelite_id, startTime, endTime, timeDelta):
    daynumber = getDayNumber(startTime)#4. november
    gnss_mapping_old = get_gnss(daynumber)

    #sjekker hver 4 time
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).total_seconds()/3600
    iterations = int(hours_between_sart_and_end/timeDelta)
 
    accuracy_time = []
    pos_list_old = []
    pos_list_new = []
    for i in range(iterations+1):
        time = pd.to_datetime(startTime)+ pd.Timedelta(hours= i*timeDelta)
        time_str = time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        daynumber2 = getDayNumber(time_str)
        gnss_mapping_new = get_gnss(daynumber2)

        #finds also the previous data because if we want to find the positions at 00:00 there may be no data in the current dataframe
        daynum2_minus_1 = int(daynumber2)  - 1
        daynumber2_minus_1 = f"{daynum2_minus_1:03d}"
        gnss_mapping_new2 = get_gnss(daynumber2_minus_1)
        #add t´the two dataframes toeachotehr
    
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        
        if satelite_id != '':
            dataframe_gnss_old = gnss_mapping_old[gnss]
            dataframe_gnss_new = gnss_mapping_new[gnss]
            dataframe_gnss_new2 = gnss_mapping_new2[gnss]

            dataframe_satellite_old =dataframe_gnss_old.loc[dataframe_gnss_old['satelite_id'] == satelite_id]
            dataframe_satellite_new =dataframe_gnss_new.loc[dataframe_gnss_new['satelite_id'] == satelite_id]
            dataframe_satellite_new2 =dataframe_gnss_new2.loc[dataframe_gnss_new2['satelite_id'] == satelite_id].tail(2)
            #adds the old dataframes to the new one
            dataframe_satellite_new = pd.concat([dataframe_satellite_new2,dataframe_satellite_new])

            positions_old = get_satellite_positions(dataframe_satellite_old,gnss,time)
            positions_new = get_satellite_positions(dataframe_satellite_new,gnss,time)

            if not (positions_new.empty or positions_old.empty):
                positionsOld, PositionsNew = position(positions_old, positions_new)
                pos_list_old.append(positionsOld)
                pos_list_new.append(PositionsNew)
                accuracy_time.append(time_str[8:10] + '/' + time_str[5:7] + ' ' + time_str[11:13])

        

    return accuracy_time, pos_list_old, pos_list_new

def positionsXYZOne(gnss,satelite_id, startTime, endTime, timeDelta):
    daynumber = getDayNumber(startTime)#4. november
    gnss_mapping_old = get_gnss(daynumber)

    #sjekker hver 4 time
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).total_seconds()/3600
    iterations = int(hours_between_sart_and_end/timeDelta)
 
    accuracy_time = []
    pos_diff = []
    diff_x = []
    diff_y = []
    diff_z = []
    for i in range(iterations+1):
        time = pd.to_datetime(startTime)+ pd.Timedelta(hours= i*timeDelta)
        time_str = time.strftime("%Y-%m-%dT%H:%M:%S.%f")
        daynumber2 = getDayNumber(time_str)
        gnss_mapping_new = get_gnss(daynumber2)

        #finds also the previous data because if we want to find the positions at 00:00 there may be no data in the current dataframe
        daynum2_minus_1 = int(daynumber2)  - 1
        daynumber2_minus_1 = f"{daynum2_minus_1:03d}"
        gnss_mapping_new2 = get_gnss(daynumber2_minus_1)
        #add t´the two dataframes toeachotehr
    
        #create a dict that has all the constellationsnames as keys and the accuracy as values
        
        if satelite_id != '':
            dataframe_gnss_old = gnss_mapping_old[gnss]
            dataframe_gnss_new = gnss_mapping_new[gnss]
            dataframe_gnss_new2 = gnss_mapping_new2[gnss]

            dataframe_satellite_old =dataframe_gnss_old.loc[dataframe_gnss_old['satelite_id'] == satelite_id]
            dataframe_satellite_new =dataframe_gnss_new.loc[dataframe_gnss_new['satelite_id'] == satelite_id]
            dataframe_satellite_new2 =dataframe_gnss_new2.loc[dataframe_gnss_new2['satelite_id'] == satelite_id].tail(2)
            #adds the old dataframes to the new one
            dataframe_satellite_new = pd.concat([dataframe_satellite_new2,dataframe_satellite_new])

            positions_old = get_satellite_positions(dataframe_satellite_old,gnss,time)
            positions_new = get_satellite_positions(dataframe_satellite_new,gnss,time)

            if not (positions_new.empty or positions_old.empty):
                positionDiff, diffx, diffy,diffz = positionXYZ(positions_old, positions_new)
                pos_diff += [positionDiff]
                diff_x += [diffx]
                diff_y += [diffy]
                diff_z += [diffz]
                accuracy_time.append(time_str[8:10] + '/' + time_str[5:7] + ' ' + time_str[11:13])

        

    return accuracy_time, pos_diff, diff_x, diff_y, diff_z

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
    plt.ylabel("MSE (km)", fontsize=14)
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
    plt.title("Distance between observed and predicted", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Distance (m)", fontsize=14)
    plt.legend(title=satelite_id, fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

def plotPos(times, pos_old, pos_new, gnss, satelite_id):

    plt.figure(figsize=(12, 6))
    
    plt.plot(times, pos_new, label = 'New Data' ,linewidth=2, marker='o')
    plt.plot(times, pos_old, label = 'Old Data' ,linewidth=2, marker='o')
    plt.grid(visible=True, linestyle='--', alpha=0.6)
    # Add labels and title
    plt.title(f"Distance from earth center for {satelite_id}", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Distance (m)", fontsize=14)
    plt.legend(title=satelite_id, fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

def plotPosXYZ(times, pos_diff, diffx, diffy,diffz, gnss, satelite_id):

    plt.figure(figsize=(12, 6))
    
    plt.plot(times, pos_diff, label = 'positions diff' ,linewidth=2)
    plt.plot(times, diffx, label = 'X diff' ,linewidth=2 )
    plt.plot(times, diffy, label = 'Y diff' ,linewidth=2 )
    plt.plot(times, diffz, label = 'Z diff' ,linewidth=2 )
    plt.grid(visible=True, linestyle='--', alpha=0.6)
    # Add labels and title
    plt.title(f"Distance from earth center for {satelite_id}", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Distance (m)", fontsize=14)
    plt.legend(title=satelite_id, fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

#find mse for all calculations
gnssList = [ 'GPS','BeiDou', 'Galileo', 'QZSS']

gnss = 'GPS'
satelite_id = 'G03'
NotAcceptedBeiDou = ['C01', 'C59', 'C02', 'C05', 'C62', 'C04', 'C03', 'C60']
# beidouSatellitesDF = pd.read_csv(f"backend/DataFrames/309/structured_dataC.csv")
# gpsDLR = pd.read_csv(f"backend/DataFrames/320/structured_dataG.csv")
# gpsIGS = pd.read_csv(f"backend/fromPHD/structured_dataG.csv")
# # beidouSatellites = beidouSatellitesDF['satelite_id'].unique()
# # gpsDLRSI = gpsDLR['satelite_id'].unique()
# # gpsIGSSI = gpsIGS['satelite_id'].unique()
# # print(f'len:{len(gpsDLRSI)}, this: {gpsDLRSI}')
# # print(f'len:{len(gpsIGSSI)}, this: {gpsIGSSI}')

# merged = pd.merge(gpsIGS, gpsDLR, on=["Datetime", "satelite_id"], suffixes=("_old", "_new"))
# columns_to_check = ["C_rs", "Delta n0", "M0", "C_uc", "e", "C_us", "sqrt(A)", "T_oe", 
#                     "C_ic", "OMEGA0", "C_is", "i0", "C_rc", "omega", "OMEGA DOT", 
#                     "IDOT", "t_tm"]

# # Dictionary to store max differences for each column
# max_differences = {}

# # Loop through the columns and compute the max difference
# for col in columns_to_check:
#     old_col = f"{col}_old"
#     new_col = f"{col}_new"
#     merged[f"{col}_diff"] = merged[old_col] - merged[new_col]
#     max_differences[col] = merged[f"{col}_diff"].max()

# # Print the results
# for col, max_diff in max_differences.items():
#     print(f"Max difference for {col}: {max_diff}")
# set1 = set(beidouSatellites)
# set2 = set(beidouSatellites5)
# set3 = set(beidouSatellites6)

# # Find the intersection of all three sets
# common_satellites = set1 & set2 & set3

# # Convert the result back to a list (optional)
# common_satellites_list = list(common_satellites)
# highErrorSatellites = {}
# for satelite_id in common_satellites_list:
#     times2, pos_diff, diffx, diffy,diffz = positionsXYZOne(gnss, satelite_id, '2024-11-04T12:00:00.000', '2024-11-06T12:00:00.000', 4)
#     if np.max(pos_diff) > 10000:
#         highErrorSatellites[satelite_id] = np.max(pos_diff)

# print(highErrorSatellites)
all = accuracyDataAll(gnssList,NotAcceptedBeiDou, '2024-11-12T12:00:00.000', '2024-11-15T12:00:00.000', 4)

#times1, acurracys = accuracyDataOne(gnss, satelite_id, '2024-11-04T12:00:00.000', '2024-11-07T12:00:00.000', 4)
#times2, pos_diff, diffx, diffy,diffz = positionsXYZOne(gnss, satelite_id, '2024-11-04T12:00:00.000', '2024-11-06T12:00:00.000', 4)
#times3, pos_list_old, pos_list_new = positionsDataOne(gnss, satelite_id, '2024-11-03T12:00:00.000', '2024-11-10T12:00:00.000', 4)

plotMultiple(gnssList, all)
#plotOne(times1, acurracys, gnss, satelite_id)
#plotPos(times3, pos_list_old, pos_list_new, gnss, satelite_id)
#plotPosXYZ(times2, pos_diff, diffx, diffy,diffz, gnss, satelite_id)
