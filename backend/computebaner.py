from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import re
import ahrs
from sortData import sortData
from datetime import datetime
from satellitePositions import get_satellite_positions

T = 558000
GM = 3.986005*10**14
we = 7.2921151467 *10**(-5) 
c = 299792458

wgs = ahrs.utils.WGS()
#romsdalen
phi = 62.42953 * np.pi/180
lam = 7.94942* np.pi/180
h = 117.5

#default nullpoint
# phi = 63.10894307441669 * np.pi/180
# lam = 10.405541695331934 * np.pi/180
# h = 115.032


def Cartesian(phi,lam, h):
    N = (wgs.a**2)/np.sqrt(wgs.a**2*(np.cos(phi))**2 + wgs.b**2*(np.sin(phi))**2)
    X = (N+h)*np.cos(phi)*np.cos(lam)
    Y = (N+h)*np.cos(phi)*np.sin(lam)
    Z = (((wgs.b**2)/(wgs.a**2))*N + h)*np.sin(phi)
    return [X,Y,Z]

#point 1 coordinates
recieverPos0 = Cartesian(phi,lam, h)

#calculate LG
T = np.matrix([[-np.sin(phi)*np.cos(lam),-np.sin(phi)*np.sin(lam) , np.cos(phi)], 
            [-np.sin(lam), np.cos(lam), 0],
            [np.cos(phi)*np.cos(lam), np.cos(phi)*np.sin(lam), np.sin(phi)]])

def CartesianToGeodetic(X,Y,Z):
    a = wgs.a
    b = wgs.b
    e2 = 1- (b**2) / (a**2)
    #1
    p = np.sqrt(X**2 + Y**2)
    #2
    phi0 = (Z/(p*(1-e**2)**(-1)))
    #3
    N0 = a**2 / np.sqrt(a**2 * np.cos(phi0)**2 + b**2 * np.sin(phi0)**2)
    h = (p / np.cos(phi0)) - N0
    phiNew = np.arctan2((Z/(p*(1-e2*N0/(N0+h)))),1)
    while phiNew != phi0:
        phi0 = phiNew
        N0 = a**2 / np.sqrt(a**2 * np.cos(phi0)**2 + b**2 * np.sin(phi0)**2)
        h = (p / np.cos(phi0)) - N0
        phiNew = np.arctan2((Z/(p*(1-e2*N0/(N0+h)))),1)

    return [phiNew*(180/np.pi),np.arctan(Y/X)*(180/np.pi),h]

#get daynumber(for broadcasting ephemeris)
def getDayNumber(date):
    print('in getDayNumber', date)
    given_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    start_date = datetime(2024, 1, 1)
    days_difference = (given_date - start_date).days + 1
    if given_date.date() == datetime.now().date():
        days_difference -= 1
    daynumber = f"{days_difference:03d}"
    print(daynumber)
    sortData(daynumber)
    return daynumber


def get_gnss(daynumber):
    print('in gnss_mapping')
    gnss_mapping = {
        'GPS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataG.csv"),
        'GLONASS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataR.csv"),
        'Galileo': pd.read_csv(f"DataFrames/{daynumber}/structured_dataE.csv"),
        'QZSS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataJ.csv"),
        'BeiDou': pd.read_csv(f"DataFrames/{daynumber}/structured_dataC.csv"),
        'NavIC': pd.read_csv(f"DataFrames/{daynumber}/structured_dataI.csv"),
        'SBAS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataS.csv")
    }
    return gnss_mapping
#same as above but it return the values that are nececary for visualizing
def visualCheck(dataframe, recieverPos0, elevationInput):
    LGDF = pd.DataFrame(columns = ["Satelitenumber","time", "X","Y","Z", "azimuth", "zenith"])
    for index, row in dataframe.iterrows():
        deltax = row["X"]-recieverPos0[0]
        deltay = row["Y"]-recieverPos0[1]
        deltaz = row["Z"]-recieverPos0[2]
        deltaCTRS = np.array([deltax,deltay,deltaz])
        
        xyzLG = T @ deltaCTRS.T
        xyzLG = np.array(xyzLG).flatten() 
        #calculate angles
        Ss = (xyzLG[0]**2 + xyzLG[1]**2 + xyzLG[2]**2)**(0.5)
        Sh = (xyzLG[0]**2 + xyzLG[1]**2 )**(0.5)
        azimuth = np.arctan2(xyzLG[1],xyzLG[0]) *180/np.pi
        zenith = np.arccos(xyzLG[2]/Ss)* 180/np.pi
        elevation = 90- abs(zenith)
        if azimuth < 0:
            azimuth = 360 + azimuth
        if(elevation >=elevationInput):
            LGDF.loc[len(LGDF)] = [row["satelite_id"],row["time"],row["X"],row["Y"],row["Z"], azimuth,zenith]
    
    return LGDF


def runData(gnss_list, elevationstring, t, epoch):
    print('in runData')
    daynumber = getDayNumber(t)
    gnss_mapping =  get_gnss(daynumber)
    elevation = float(elevationstring)
    #create a list that contains the seconds for every halfhour in the epoch when epoch is hours
    final_list = []
    final_listdf = []
    print('finds visual satellites')
    for i in range(0, int(epoch)*4):
        time = pd.to_datetime(t)+ pd.Timedelta(minutes=i*15)
        LGDF_dict = []
        LGDF_df = []
        for gnss in gnss_list:
            positions = get_satellite_positions(gnss_mapping[gnss],gnss,time)
            data = visualCheck(positions, recieverPos0, elevation)
            if not data.empty:
                LGDF_dict += [data.to_dict()]  
                LGDF_df += [data]
        final_list.append(LGDF_dict)
        final_listdf.append(LGDF_df)
    return final_list, final_listdf

def accuracy(positions_orginal, positions_2):
    print('in accuracy')
    #calculate the difference between the two dataframes
    positions = pd.merge(positions_orginal, positions_2, on = "satelite_id", suffixes = ("_orginal", "_2"))
    positions["X_diff"] = positions["X_orginal"] - positions["X_2"]
    positions["Y_diff"] = positions["Y_orginal"] - positions["Y_2"]
    positions["Z_diff"] = positions["Z_orginal"] - positions["Z_2"]
    positions["distance"] = np.sqrt(positions["X_diff"]**2 + positions["Y_diff"]**2 + positions["Z_diff"]**2)
    #calculate the average accuracy
    averageAccuracy = positions["distance"].mean()
    return averageAccuracy

def accuracyData(gnss_list, startTime, endTime, timeDelta):
    print('in accuracyData')
    daynumber = getDayNumber(startTime)
    gnss_mapping_orginal = gnss_mapping(daynumber)
    #create a list that contains the seconds for every halfhour in the epoch when epoch is hours
    hours_between_sart_and_end = (pd.to_datetime(endTime) - pd.to_datetime(startTime)).seconds/3600
    iterations = int(hours_between_sart_and_end/timeDelta)
    print('calculating accurracy')
    accuracy_dict_time = {}
    for i in range(iterations):
        print(f'iteration {i}')
        time = pd.to_datetime(startTime)+ pd.Timedelta(hours= i*timeDelta)
        daynumber2 = getDayNumber(time)
        gnss_mapping_2 = gnss_mapping(daynumber2)
        accuracy_dict= {}
        for gnss in gnss_list:
            positions_orginal = get_satellite_positions(gnss_mapping_orginal[gnss],gnss,time)
            positions_2 = get_satellite_positions(gnss_mapping_2[gnss],gnss,time)
            if not (positions_2.empty or positions_orginal.empty):
                averageAccuracy = accuracy(positions_orginal, positions_2)
                accuracy_dict[gnss] = averageAccuracy

        accuracy_dict_time[time] = accuracy_dict

    return accuracy_dict_time
# test funksjoner
# def visualCheck2(dataframe, recieverPos0, elevationInput):
#     LGDF = pd.DataFrame(columns = ["satelite_id","time", "X","Y","Z", "azimuth", "zenith"])
#     for index, row in dataframe.iterrows():
#         deltax = row["X"]-recieverPos0[0]
#         deltay = row["Y"]-recieverPos0[1]
#         deltaz = row["Z"]-recieverPos0[2]
#         deltaCTRS = np.array([deltax,deltay,deltaz])
        
#         xyzLG = T @ deltaCTRS.T
#         xyzLG = np.array(xyzLG).flatten() 
#         #calculate angles
#         Ss = (xyzLG[0]**2 + xyzLG[1]**2 + xyzLG[2]**2)**(0.5)
#         Sh = (xyzLG[0]**2 + xyzLG[1]**2 )**(0.5)
#         azimuth = np.arctan2(xyzLG[1],xyzLG[0]) *180/np.pi
#         zenith = np.arccos(xyzLG[2]/Ss)* 180/np.pi
#         elevation = 90- abs(zenith)
#         print(elevation, elevationInput)
#         if azimuth < 0:
#             azimuth = 360 + azimuth
#         if(elevation >=elevationInput):
#             LGDF.loc[len(LGDF)] = [row["satelite_id"],row["time"],row["X"],row["Y"],row["Z"], azimuth,zenith]
    
#     return LGDF



# def runData3(gnss_list, elevationstring, t, str, recpos):
#     daynumber = "345"    
#     gnss_mapping = {
#         'GPS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataG.csv"),
#         'Galileo': pd.read_csv(f"DataFrames/{daynumber}/structured_dataE.csv"),
#         'GLONASS': pd.read_csv(f"DataFrames/{daynumber}/structured_dataR.csv"),
#         'BeiDou': pd.read_csv(f"DataFrames/{daynumber}/structured_dataC.csv"),

#     }
#     elevation = float(elevationstring)
#     #create a list that contains the seconds for every halfhour in the epoch when epoch is hours
#     with open (f'{str}.csv','w') as f:
#         f.write(f"Satellitenumber,time,X,Y,Z,zenith, azimuth\n")
#         for i in range(0, 1):
#             time = pd.to_datetime(t)+ pd.Timedelta(seconds=i)
    
#             for gnss in gnss_list:
#                 positions = get_satellite_positions(gnss_mapping[gnss],gnss,time)

#                 if not positions.empty:
#                     visual = visualCheck2(positions, recpos, 10)
#                     for index, row in visual.iterrows():
                        
#                         f.write(f"{row['satelite_id']}, {row['time']}, {row['X']}, {row['Y']}, {row['Z']} ,{row['zenith']}, {row['azimuth']}\n")
            
#         f.close() 
    

