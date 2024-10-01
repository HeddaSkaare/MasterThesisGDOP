
import itertools
import numpy as np
import pandas as pd
import ahrs
from computebaner import runData
# from satellitePositions import cartesianGPS

T = 558000
GM = 3.986005*10**14
we = 7.2921151467 *10**(-5) 
c = 299792458
wgs = ahrs.utils.WGS()
#romsdalen
phi = 62.42953 * np.pi/180
lam = 7.94942* np.pi/180
h = 117.5
def Cartesian(phi,lam, h):
    N = (wgs.a**2)/np.sqrt(wgs.a**2*(np.cos(phi))**2 + wgs.b**2*(np.sin(phi))**2)
    X = (N+h)*np.cos(phi)*np.cos(lam)
    Y = (N+h)*np.cos(phi)*np.sin(lam)
    Z = (((wgs.b**2)/(wgs.a**2))*N + h)*np.sin(phi)
    return [X,Y,Z]

#point 1 coordinates
recieverPos0 = Cartesian(phi,lam, h)
def geometric_range(sat_pos, rec_pos):
    return np.sqrt((sat_pos[0] - rec_pos[0])**2 +
                   (sat_pos[1] - rec_pos[1])**2 +
                   (sat_pos[2] - rec_pos[2])**2)


def DOPvalues(satellites, recieverPos0):
    size = len(satellites)
    A = np.zeros((size, 4))  
    Qxx =np.zeros((4, 4)) 
    #creates the A matrix
    i = 0
    for satellite in satellites:
        rho_i = geometric_range([satellite[2], satellite[3], satellite[4]], recieverPos0)
        A[i][0] = -(satellite[2]-recieverPos0[0]) / rho_i
        A[i][1] = -(satellite[3] - recieverPos0[1]) / rho_i
        A[i][2] = -(satellite[4] - recieverPos0[2] ) / rho_i
        A[i][3] = -c 
        i +=1

    AT = A.T
    ATA = AT@A
    Qxx = np.linalg.inv(ATA)
    GDOP = np.sqrt(Qxx[0][0] + Qxx[1][1] + Qxx[2][2] + Qxx[3][3])
    PDOP = np.sqrt(Qxx[0][0] + Qxx[1][1] + Qxx[2][2])
    TDOP = np.sqrt(Qxx[3][3])

    return GDOP,PDOP,TDOP

def best(satellites):
    final_DOP_values = []
    for satelitedf in satellites:
        satellites_array = []
        for satellitedf in satelitedf:
            for index,row in satellitedf.iterrows():
                satellites_array += [[row["Satelitenumber"],row["time"], row["X"],row["Y"], row["Z"]]]
        if(len(satellites_array) > 0):
            GDOP, PDOP, TDOP = DOPvalues(satellites_array, recieverPos0)
            final_DOP_values.append([GDOP, PDOP, TDOP])
        else:
            final_DOP_values.append([0, 0, 0])
    
    return final_DOP_values
