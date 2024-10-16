import math
import pandas as pd
import numpy as np
import re
import ahrs

#common functions
T = 558000
GM = 3.986005*10**14
we = 7.2921151467 * 10**(-5) 
c = 299792458

def TS(P,c,dt):
    return T-(P/c) + dt
def TK(t):
    tm = t
    if(t >302400):
        return tm-604800
    elif(t <-302400 ):
        return tm+604800
    else:
        return tm

def MK(M0, a,deltan, tk):
    return M0 + (np.sqrt(GM/a**3)+deltan)*tk

def EK(Mk,e, n):
    E = [Mk]
    for i in range(1,n):
        Enew = E[i-1] + ((Mk-E[i-1]+e*np.sin(E[i-1]))/(1-e*np.cos(E[i-1])))
        E.append(Enew)
    return Mk + e*np.sin(E[-1])

def FK(e,Ek):
    return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(Ek/2))

def UK(w,fk,Cuc,Cus):
    return w+ fk + Cuc*(np.cos(2*(w+fk))) + Cus*(np.sin(2*(w+fk)))

def RK(a,e,w,Ek,fk,Crc,Crs):
    return a*(1-e*np.cos(Ek)) + Crc*(np.cos(2*(w+fk))) + Crs*(np.sin(2*(w+fk)))

def IK(i0,idot,tk,Cic,w,fk,Cis):
    return i0+ idot*tk + Cic*(np.cos(2*(w+fk))) + Cis*(np.sin(2*(w+fk)))

def LAMBDAK(lambda0,omegadot,we,tk,toe):
    return lambda0 + (omegadot-we)*tk - we*toe


def R1(theta):
    return np.array([[1,0,0],[0,np.cos(theta),np.sin(theta)],[0,-np.sin(theta),np.cos(theta)]])
def R3(theta):
    return np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1]])

def cartesianB_list(data, time):
    diff = 720100000000
    theIndex = 0
    i = 0
    #find the Datetime that is closes to time, but the datetime has to beback in time compared to time
    for index, row in data.iterrows():
        if (row["Datetime"] < time) and ((time-row["Datetime"]).total_seconds() < diff):
            theIndex = i
            diff = (time-row["Datetime"]).total_seconds()
        i += 1
    row = data.iloc[theIndex]
    satelite_id = row["satelite_id"]
    tk = TK(diff)
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek,fk, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM

    return [satelite_id,time.strftime("%Y-%m-%dT%H:%M:%S.%f"), coordinates[0], coordinates[1],coordinates[2]]

def cartesianC_list(data, time):
    diff = 18000000000000
    prevRow = []
    endRow = []
    if not data.empty:
        for index, row in data.iterrows():
            
            if (row["Datetime"] < time) and ((time-row["Datetime"]).total_seconds() < diff):
                diff = (time-row["Datetime"]).total_seconds()
                #bergener farten selv
                
                if not len(prevRow) == 0:
                    prevTime = (row["Datetime"]-prevRow[0]).total_seconds()
                    vx = 1000*(row["X"]-prevRow[1])/prevTime
                    vy = 1000*(row["Y"]-prevRow[2])/prevTime
                    vz = 1000*(row["Z"]-prevRow[3])/prevTime
                    x = row["X"]*1000 + vx*diff 
                    y = row["Y"]*1000 + vy*diff
                    z = row["Z"]*1000 + vz*diff
                    endRow = [row["satelite_id"],time.strftime("%Y-%m-%dT%H:%M:%S.%f"), x, y,z]
                else:
                    x = (row["X"] + row["Vx"]*diff + 0.5*row["ax"]*diff**2)*1000
                    y = (row["Y"] + row["Vy"]*diff + 0.5*row["ay"]*diff**2)*1000
                    z = (row["Z"] + row["Vz"]*diff + 0.5*row["az"]*diff**2)*1000
                    endRow = [row["satelite_id"],time.strftime("%Y-%m-%dT%H:%M:%S.%f"), x, y,z] 
            prevRow = [row['Datetime'], row["X"], row["Y"],row["Z"]] 
    return endRow

#kommer annenhver time 7200 sek
def cartesianA_list(data, time):
    #obs = pd.read_csv("test/test1.csv")
    diff = 7201000000
    theIndex = 0
    i = 0
    #find the Datetime that is closes to time, but the datetime has to beback in time compared to time
    for index, row in data.iterrows():
        if (row["Datetime"] < time) and ((time-row["Datetime"]).total_seconds() < diff):
            theIndex = i
            diff = (time-row["Datetime"]).total_seconds()
        i += 1
    row = data.iloc[theIndex]
    satelite_id = row["satelite_id"]
    #sjekk om denne satelittiden eksisterer i obs
    # if satelite_id in obs['Satellitenumber'].values:
    #     obsRow = obs.loc[obs['Satellitenumber'] == satelite_id]
    #     diffe = float(diff - (obsRow['P']/c) + obsRow['dt'])
        
    #     tk = TK(diffe)
    # else:
    #     tk = TK(diff)
    tk = TK(diff)
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n0"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek,fk, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])
    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM 


    return [satelite_id, time.strftime("%Y-%m-%dT%H:%M:%S.%f") , coordinates[0], coordinates[1],coordinates[2]] 

def get_satellite_positions(data,gnss,time):
    
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    dataGrouped = data.groupby("satelite_id")
    positions = pd.DataFrame(columns = ["satelite_id","time", "X", "Y", "Z" ])
    if(gnss == "GPS") or (gnss == "Galileo"):
        for key, group in dataGrouped:
            if(cartesianA_list(group, time) != []):
                positions.loc[len(positions)] = cartesianA_list(group, time)
    elif(gnss == "GLONASS") or (gnss == "SBAS"):
        for key, group in dataGrouped:
            if(cartesianC_list(group, time) != []):
                positions.loc[len(positions)] = cartesianC_list(group, time)
    elif(gnss == "BeiDou") or (gnss == "QZSS") or (gnss == "IRNSS"):
        for key, group in dataGrouped:
            if(cartesianB_list(group, time) != []):
                positions.loc[len(positions)] = cartesianB_list(group, time)
    print(positions)
    return positions

#testing

# def get_satellite_positiontest(data,gnss,time):
#     data['Datetime'] = pd.to_datetime(data['Datetime'])
#     dataGrouped = data.groupby("satelite_id")
#     time = pd.to_datetime(time)
#     positions = pd.DataFrame(columns = ["satelite_id","TOW", "X", "Y", "Z" ])
#     if(gnss == "GPS") or (gnss == "Galileo"):
#         for key, group in dataGrouped:
#             if(cartesianA_list(group, time) != []):
#                 positions.loc[len(positions)] = cartesianA_list(group, time)
#     elif(gnss == "GLONASS") or (gnss == "SBAS"):
#         for key, group in dataGrouped:
#             if(cartesianC_list(group, time) != []):
#                 positions.loc[len(positions)] = cartesianC_list(group, time)
#     elif(gnss == "BeiDou") or (gnss == "QZSS") or (gnss == "IRNSS"):
#         for key, group in dataGrouped:
#             if(cartesianB_list(group, time) != []):
#                 positions.loc[len(positions)] = cartesianB_list(group, time)
#     return positions