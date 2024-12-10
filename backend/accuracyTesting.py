


from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from computeDOP import best
from computebaner import get_gnss, getDayNumber, visualCheck
from satellitePositions import get_satellite_positions

phi = 62.42953 * np.pi/180
lam = 7.94942* np.pi/180
h = 117.5
recieverPos = [phi, lam, h] 

#the mse function
def MSE(positions_old, positions_new):
    
    #calculate the difference between the two dataframes
    positions = pd.merge(positions_old, positions_new, on = "satelite_id", suffixes = ("_old", "_new"))
    #positions = positions[~positions['satelite_id'].isin(notAcceptedSatellites)]
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
    #print(positions_old)
    positions_old["distanceBetween"] = (np.sqrt((positions_new["X"]-positions_old["X"])**2 + (positions_new["Y"]-positions_old["Y"])**2 + (positions_new["Z"]-positions_old["Z"])**2))
    positions_old["distanceX"] = (positions_new["X"]-positions_old["X"])
    positions_old["distanceY"] = (positions_new["Y"]-positions_old["Y"])
    positions_old["distanceZ"] = (positions_new["Z"]-positions_old["Z"]) 
    #calculate the average accuracy
    
    return positions_old["distanceBetween"] , positions_old["distanceX"], positions_old["distanceY"], positions_old["distanceZ"]

#positions based on first date
def accuracyDataAll(gnss_list, startTime, endTime, timeDelta):

    daynumber = getDayNumber(startTime)#4. november
    gnss_mapping_old = get_gnss(daynumber)
    daynum_minus_1 = int(daynumber)  - 1
    daynumber_minus_1 = f"{daynum_minus_1:03d}"
    gnss_mapping_old1 = get_gnss(daynumber_minus_1)

    #sjekker hver 4 time
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).total_seconds() /3600
    iterations = int(hours_between_sart_and_end/timeDelta)

    final_list_old = []
    final_list_new = []
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
        LGDF_df_old = []
        LGDF_df_new = []
        for gnss in gnss_list:
            dataframe_satellite_new2 = gnss_mapping_new2[gnss]
       
            newDataframe2 = pd.concat([gnss_mapping_new[gnss], dataframe_satellite_new2])
            newDataframe1 = pd.concat([gnss_mapping_old[gnss], gnss_mapping_old1[gnss]])


            positions_old = get_satellite_positions(newDataframe1,gnss,time)
            positions_new = get_satellite_positions(newDataframe2,gnss,time)
            # print(f'positions old: {positions_old}')
            # print(f'positions new: {positions_new}')
            if not (positions_new.empty or positions_old.empty):
                averageMSE = MSE(positions_old, positions_new)
                accuracy_dict[gnss].append(averageMSE)
                visualSatellites_new = visualCheck(positions_new, recieverPos, 10)
                visualSatellites_old = visualCheck(positions_old, recieverPos, 10)
                LGDF_df_old.append(visualSatellites_old)
                LGDF_df_new.append(visualSatellites_new)
        
        final_list_old.append(LGDF_df_old)
        final_list_new.append(LGDF_df_new)
        accuracy_dict_time[time_str] = accuracy_dict

    return accuracy_dict_time, final_list_old, final_list_new




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
    plt.ylabel("Distance (m)", fontsize=14)
    plt.legend(title="GNSS", fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

def plotPosXYZ(times, pos_diff, diffx, diffy,diffz, gnss, satelite_id):
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(times[3:10], pos_diff[3:10], label = 'positions diff' ,linewidth=2)
    plt.plot(times[3:10], diffx[3:10], label = 'X diff' ,linewidth=2 )
    plt.plot(times[3:10], diffy[3:10], label = 'Y diff' ,linewidth=2 )
    plt.plot(times[3:10], diffz[3:10], label = 'Z diff' ,linewidth=2 )
    plt.grid(visible=True, linestyle='--', alpha=0.6)
    # Add labels and title
    plt.title(f"Distance between predicted and true satellite positions for {gnss}: {satelite_id}", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Distance (m)", fontsize=14)
    plt.legend(title=satelite_id, fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    # Show plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()
def plotDOP(doplist_new, doplist_old, time):
    PDOP_new = []
    HDOP_new = []
    VDOP_new = []
    PDOP_old = []
    HDOP_old = []
    VDOP_old = []
    HDOP_diff = []
    VDOP_diff = []
    PDOP_diff = []
    for i in range(len(doplist_new)):
        PDOP_new.append(doplist_new[i][2])
        HDOP_new.append(doplist_new[i][3])
        VDOP_new.append(doplist_new[i][4])
        PDOP_old.append(doplist_old[i][2])
        HDOP_old.append(doplist_old[i][3])
        VDOP_old.append(doplist_old[i][4])
        PDOP_diff.append(doplist_new[i][2] - doplist_old[i][2])
        HDOP_diff.append(doplist_new[i][3] - doplist_old[i][3])
        VDOP_diff.append(doplist_new[i][4] - doplist_old[i][4])
        
    
    plt.figure(figsize=(12, 6))
    plt.title(f"DOP values over time", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Dilution of precision ", fontsize=14)
    plt.plot(time, PDOP_new, label = 'PDOP new',linewidth=2)
    plt.plot(time, HDOP_new, label = 'HDOP new',linewidth=2)
    plt.plot(time, VDOP_new, label = 'VDOP new',linewidth=2)
    plt.plot(time, PDOP_old, label = 'PDOP old',linewidth=2)
    plt.plot(time, HDOP_old, label = 'HDOP old',linewidth=2)
    plt.plot(time, VDOP_old, label = 'VDOP old',linewidth=2)
    plt.legend( fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.title(f"Difference in DOP values", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Dilution of precision difference ", fontsize=14)
    plt.plot(time, PDOP_diff, label = 'PDOP diff',linewidth=2)
    plt.plot(time, HDOP_diff, label = 'HDOP diff',linewidth=2)
    plt.plot(time, VDOP_diff, label = 'VDOP diff',linewidth=2)
    plt.legend(fontsize=12, title_fontsize=14, loc='best')
    plt.xticks(rotation=45, fontsize=12)
    plt.tight_layout()  # Adjust layout to fit everything nicely
    plt.show()

    

#find mse for all calculations
gnssList = [ 'GPS','BeiDou', 'Galileo', 'QZSS']


satellite =[ 'G24','C24', 'E07', 'J04']
distance_to_earth = [20182500,21528000, 23222000, 35791500]

# all, final_old, final_new = accuracyDataAll(gnssList, '2024-11-04T12:00:00.000', '2024-11-07T12:00:00.000', 4)
# plotMultiple(gnssList, all)

for i in range(len(satellite)):#len(satellite)
    times2, pos_diff, diffx, diffy,diffz = positionsXYZOne(gnssList[i], satellite[i], '2024-11-04T12:00:00.000', '2024-11-07T12:00:00.000', 4)
    #plotPosXYZ(times2, pos_diff, diffx, diffy,diffz, gnssList[i], satellite[i])
    lengste_avstand = np.max(pos_diff)

    vinkel =  2* np.arcsin((lengste_avstand/2)/distance_to_earth[i])* 180/np.pi
    print(f'satellite: {satellite[i]}, distance: {lengste_avstand} vinkel: {vinkel}')


# #lag prot for dop også

# dop_old = best(final_old)
# dop_new = best(final_new)
# print("old",dop_old)
# print("new:",dop_new)
# plotDOP(dop_new, dop_old, times2)


# phi = 63.41458293  * np.pi/180
# lam = 10.41044691  * np.pi/180
# h =39.689
# recieverPos = [phi,lam,h]
# df = pd.read_csv('backend/DataFrames/332/structured_dataR.csv')

# timeDate = pd.to_datetime('2024-11-27T14:32:15.000')
# pos = get_satellite_positions(df,'GLONASS',timeDate)
# print(pos)
# otherPos = visualCheck(pos, recieverPos, 10)
# print(otherPos)