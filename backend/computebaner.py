from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import re
import ahrs
#from sortData import structured_dataG, structured_dataR, structured_dataE, structured_dataJ, structured_dataC, structured_dataI, structured_dataS
#from satellitePositions import cartesianA_list, cartesianB_list, cartesianC_list, cartesianGPS, cartesianBeiDou,cartesianGalileo,cartesianGLONASS,cartesianNavIC,cartesianQZSS,cartesianSBAS
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

dataGPS = pd.read_csv("DataFrames/269/rawdfGPS.csv")
dataGLONASS = pd.read_csv("DataFrames/269/rawdfGLONASS.csv")
dataBeiDou = pd.read_csv("DataFrames/269/rawdfBeiDou.csv")
dataGalileo = pd.read_csv("DataFrames/269/rawdfGalileo.csv")
dataQZSS = pd.read_csv("DataFrames/269/rawdfQZSS.csv")
dataNavIC = pd.read_csv("DataFrames/269/rawdfIRNSS.csv")
dataSBAS = pd.read_csv("DataFrames/269/rawdfSBAS.csv")


gnss_mapping = {
    'GPS': dataGPS,
    'GLONASS': dataGLONASS,
    'Galileo': dataGalileo,
    'QZSS': dataQZSS,
    'BeiDou': dataBeiDou,
    'NavIC': dataNavIC,
    'SBAS': dataSBAS
}
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
        elevation = 90- zenith
        if azimuth < 0:
            azimuth = 360 + azimuth
        if(elevation >=elevationInput):
            LGDF.loc[len(LGDF)] = [row["satelite_id"],row["time"],row["X"],row["Y"],row["Z"], azimuth,zenith]
    
    return LGDF

def runData(gnss_list, elevationstring, t, epoch):
    elevation = float(elevationstring)
    #create a list that contains the seconds for every halfhour in the epoch when epoch is hours
    final_list = []
    final_listdf = []
    for i in range(0, int(epoch)*2):
        time = pd.to_datetime(t)+ pd.Timedelta(minutes=i*30)
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
 


