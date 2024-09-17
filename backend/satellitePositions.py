import math
import pandas as pd
import numpy as np
import re
import ahrs
from sortData import structured_dataG, structured_dataR, structured_dataE, structured_dataJ, structured_dataC, structured_dataI, structured_dataS

#common functions
T = 558000
GM = 3.986005*10**14
we = 7.2921151467 *10**(-5) 
c = 299792458

def TS(P,c,dt):
    return T-(P/c) + dt
def TK(t_tm):
    if math.isnan(t_tm) :
        t_tm = 0.9999e+9 -604800

    if(t_tm >302400):
        return t_tm-604800
    elif(t_tm <-302400 ):
        return t_tm+604800
    else:
        return t_tm

def MK(M0, a,deltan, tk):
    return M0 + (np.sqrt(GM/a**3)+deltan)*tk

def EK(Mk,e, n):
    E = [Mk]
    for i in range(1,n):
        Enew = E[i-1] + (Mk-E[i-1]+e*np.sin(E[i-1]))/(1-e*np.cos(E[i-1]))
        E.append(Enew)
    return Mk + e*np.sin(E[-1])

def FK(e,Ek):
    return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(Ek/2))

def UK(w,fk,Cuc,Cus):
    return w+fk+Cuc*(np.cos(w+fk))**2+ Cus*(np.sin(w+fk))**2

def RK(a,e,w,Ek,Crc,Crs):
    return a*(1-e*np.cos(Ek))+Crc*(np.cos(w+fk))**2+ Crs*(np.sin(w+fk))**2
def IK(i0,idot,tk,Cic,w,fk,Cis):
    return i0+idot*tk + +Cic*(np.cos(w+fk))**2+ Cis*(np.sin(w+fk))**2
def LAMBDAK(lambda0,omegadot,we,tk,toe):
    return lambda0+(omegadot-we)*tk-we*toe

def R1(theta):
    return np.array([[1,0,0],[0,np.cos(theta),np.sin(theta)],[0,-np.sin(theta),np.cos(theta)]])
def R3(theta):
    return np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1]])



#GPS
cartesianGPS = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])

for index, row in structured_dataG.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    #ts = 0.07#TS(P,c,dtj)
    tk = TK(row["t_tm"])
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n0"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
    cartesianGPS.loc[len(cartesianGPS)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]  


#GLONASS

cartesianGLONASS = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])

for index, row in structured_dataR.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    cartesianGLONASS.loc[len(cartesianGLONASS)] = [satelite_id,time, row["X"], row["Y"],row["Z"]]  

#Galileo
cartesianGalileo = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])
for index, row in structured_dataE.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    tk = TK(row["t_tm"])
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n0"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
    cartesianGalileo.loc[len(cartesianGalileo)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]

#QZSS

cartesianQZSS = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])
for index,row in structured_dataJ.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    tk = TK(row["t_tm"])
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
    cartesianQZSS.loc[len(cartesianQZSS)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]

#SBAS
cartesianSBAS = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])
for index,row in structured_dataS.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    cartesianSBAS.loc[len(cartesianSBAS)] = [satelite_id,time, row["X"], row["Y"],row["Z"]]

#IRNSS
cartesianNavIC = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])

for index, row in structured_dataI.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    tk = TK(row["t_tm"])
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
    cartesianNavIC.loc[len(cartesianNavIC)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]

#BeiDou
cartesianBeiDou = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])
for index,row in structured_dataC.iterrows():
    satelite_id = row["satelite_id"]
    time = row["Datetime"]
    tk = TK(row["t_tm"])
    Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n"], tk)
    Ek = EK(Mk,row["e"],3)
    fk = FK(row["e"],Ek)
    uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
    rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
    ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
    lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

    rkM = np.array([rk,0,0]).transpose()
    coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
    cartesianBeiDou.loc[len(cartesianBeiDou)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]