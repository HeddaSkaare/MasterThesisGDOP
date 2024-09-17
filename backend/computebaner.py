from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import re
import ahrs
from sortData import structured_dataG, structured_dataR, structured_dataE, structured_dataJ, structured_dataC, structured_dataI, structured_dataS
from satellitePositions import cartesianGPS, cartesianBeiDou,cartesianGalileo,cartesianGLONASS,cartesianNavIC,cartesianQZSS,cartesianSBAS

T = 558000
GM = 3.986005*10**14
we = 7.2921151467 *10**(-5) 
c = 299792458

# content = []
# with open("data.txt", "r") as file:
#     content = file.read()


# split_index = content.index("END OF HEADER")
# header_part = content[:split_index] # baneinformasjon
# data_part = content[split_index+13:] #satelitt informasjon

# # Steg 1: Splitte data etter satellittetikettene
# satellitt_data = data_part.split("G")[1:]  # Fjerner eventuell tom tekst før første G
# def split_on_second_sign(s):
#     # Finn posisjoner av pluss- og minus-tegnene som ikke er etterfulgt av 'D'
#     signs = [m.start() for m in re.finditer(r'(?<!D)[+-]', s)]
    
#     # Hvis det ikke er noen tegn, returner strengen som den er
#     if not signs:
#         return s

#     # Start splitting basert på antall funn
#     parts = []
#     last_index = 0
#     for idx in signs:
#         parts.append(s[last_index:idx])  # Legg til delen før tegnet
#         last_index = idx  # Oppdater startposisjonen til det neste segmentet
    
#     # Legg til siste del av strengen etter det siste tegnet
#     parts.append(s[last_index:])
    
#     return parts
# def flatten(lst):
#     flat_list = []
#     for item in lst:
#         if isinstance(item, (list, tuple)):
#             flat_list.extend(item)  # Legg til alle elementer i item
#         else:
#             flat_list.append(item)  # Hvis ikke, legg til elementet direkte
#     return flat_list
# def strToFloat(inputstring):
#     splittedString = inputstring.split("D")
#     num = float(splittedString[0])
#     potens = int(splittedString[1])
#     return num * 10**potens
# # Steg 2: Strukturere dataene i en dictionary
# structured_data = {}
# ekstra_data = {"G08":{"PL1":22550792.660 , "dtj": 0.00013345632 , "dion": 3.344, "drop":4.055},
#                "G10":{"PL1":22612136.900  , "dtj": 0.000046155711  , "dion": 2.947, "drop":4.297},
#                 "G21":{"PL1":20754631.240  , "dtj": -0.00015182034  , "dion": 2.505, "drop":2.421},
#                 "G24":{"PL1":23974471.500  , "dtj": 0.00026587520 , "dion": 3.644, "drop":9.055},
#                "G17":{"PL1":24380357.760, "dtj": -0.00072144074 , "dion": 6.786, "drop":9.756,},
#                "G03":{"PL1":24444143.500, "dtj": 0.00022187057, "dion": 4.807, "drop":10.863},
#                "G14":{"PL1":22891323.280, "dtj": -0.00013020719 , "dion": 4.598, "drop":4.997}}
# for entry in satellitt_data:
#     lines = entry.strip().splitlines()
#     satellitt_id = "G" + lines[0].split()[0]  # Første linje inneholder satellitt-ID (f.eks. G08)
    
#     # Slå sammen tallene i en enkelt liste, fjerner ID og tid fra første linje
#     forsteLinje = lines[0].split()[1:]
#     tall = " ".join(lines[1:]).split()  # Kombinerer linjene og splittes på mellomrom
#     flattened_forstelinje = flatten(list(map(split_on_second_sign, forsteLinje)))
#     flattened_tall = flatten(list(map(split_on_second_sign, tall)))
#     cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']
#     IODE = cleaned_forstelinje[:5]
#     #satelittNavn = f"{satellitt_id} {IODE[2]}.{IODE[1]}.{IODE[0]} kl.{IODE[3]}:{IODE[4]}"
#     info_forstelinje = cleaned_forstelinje[6:]
#     cleaned_tall = [item for item in flattened_tall if item != '']
#     finalInfoList = []
#     finalTallList = []
#     for value in info_forstelinje:
#         floatNumber = strToFloat(value)
#         finalInfoList += [floatNumber]
#     for value in cleaned_tall:
#         floatNumber = strToFloat(value)
#         finalTallList += [floatNumber]
#     structured_data[satellitt_id] = finalInfoList +finalTallList




# # Opprette en pandas DataFrame
# df = pd.DataFrame(structured_data)


# def R1(theta):
#     return np.array([[1,0,0],[0,np.cos(theta),np.sin(theta)],[0,-np.sin(theta),np.cos(theta)]])
# def R3(theta):
#     return np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1]])


# #task 1
# def TS(P,c,dt):
#     return T-(P/c) + dt
# def TK(t_tm):
#     if(t_tm >302400):
#         return t_tm-604800
#     elif(t_tm <-302400 ):
#         return t_tm+604800
#     else:
#         return t_tm

# def MK(M0, a,deltan, tk):
#     return M0 + (np.sqrt(GM/a**3)+deltan)*tk

# def EK(Mk,e, n):
#     E = [Mk]
#     for i in range(1,n):
#         Enew = E[i-1] + (Mk-E[i-1]+e*np.sin(E[i-1]))/(1-e*np.cos(E[i-1]))
#         E.append(Enew)
#     return Mk + e*np.sin(E[-1])

# def FK(e,Ek):
#     return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(Ek/2))

# def UK(w,fk,Cuc,Cus):
#     return w+fk+Cuc*(np.cos(w+fk))**2+ Cus*(np.sin(w+fk))**2

# def RK(a,e,w,Ek,Crc,Crs):
#     return a*(1-e*np.cos(Ek))+Crc*(np.cos(w+fk))**2+ Crs*(np.sin(w+fk))**2
# def IK(i0,idot,tk,Cic,w,fk,Cis):
#     return i0+idot*tk + +Cic*(np.cos(w+fk))**2+ Cis*(np.sin(w+fk))**2
# def LAMBDAK(lambda0,omegadot,we,tk,toe):
#     return lambda0+(omegadot-we)*tk-we*toe

# #with the correction
# print("With correction")
# cartesianGPS = pd.DataFrame(columns = ["Satelite number","time", "X", "Y", "Z", ])


# for index, row in structured_dataG.iterrows():
#     satelite_id = row["satelite_id"]
#     time = row["Datetime"]
#     #ts = 0.07#TS(P,c,dtj)
#     tk = TK(row["t_tm"])
#     Mk = MK(row["M0"],row["sqrt(A)"]**2, row["Delta n0"], tk)
#     Ek = EK(Mk,row["e"],3)
#     fk = FK(row["e"],Ek)
#     uk = UK(row["omega"], fk,row["C_uc"],row["C_us"])
#     rk = RK(row["sqrt(A)"]**2, row["e"], row["omega"], Ek, row["C_rc"],row["C_us"])
#     ik = IK(row["i0"],row["IDOT"],tk,row["C_ic"],row["omega"],fk,row["C_is"])
#     lambdak= LAMBDAK(row["OMEGA0"],row["OMEGA DOT"], we,tk,row["T_oe"])

#     rkM = np.array([rk,0,0]).transpose()
#     coordinates = R3(-lambdak)@R1(-ik)@R3(-uk)@rkM
#     cartesianGPS.loc[len(cartesianGPS)] = [satelite_id,time, coordinates[0], coordinates[1],coordinates[2]]  
    
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


#example data
# lam = 10.58311814 * np.pi/180
# phi  = 63.40919533 *np.pi/180
# deltax = 1084.518
# deltay = -9212.999
# deltaz = -87.373
#calculate LG
T = np.matrix([[-np.sin(phi)*np.cos(lam),-np.sin(phi)*np.sin(lam) , np.cos(phi)], 
            [-np.sin(lam), np.cos(lam), 0],
            [np.cos(phi)*np.cos(lam), np.cos(phi)*np.sin(lam), np.sin(phi)]])

def CartesianToGeodetic(X,Y,Z):
    a = wgs.a
    b = wgs.b
    e = np.sqrt((a**2 - b**2) / (a**2))
    p = np.sqrt(X**2+Y**2)
    phi0 = (Z/p)*(1-e**2)**(-1)
    N0 = (a**2)/np.sqrt((a**2)*(np.cos(phi0)**2) + (b**2)*(np.sin(phi0)**2))
    h = (p/np.cos(phi0))-N0
    phiNew = np.arctan((Z/p)*(1-(e**2)*(N0/(N0+h))**(-1)))

    while phiNew != phi0:
        phi0 = phiNew
        N0 = (a**2)/np.sqrt((a**2)*(np.cos(phi0)**2) + (b**2)*(np.sin(phi0)**2))
        h = (p/np.cos(phi0))- N0
        phiNew = np.arctan((Z/p)*(1-(e**2)*(N0/(N0+h))**(-1)))

    return [phiNew*(180/np.pi),np.arctan(Y/X)*(180/np.pi),h]

def angles(dataframe, recieverPos0):
    LGDF = pd.DataFrame(columns = ["Satelite number","time", "LGcoords", "Ss", "Sh", "azimuth", "zenith", "elevation"])
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
        azimuth = np.arctan(xyzLG[1]/xyzLG[0]) *180/np.pi
        zenith = np.arccos(xyzLG[2]/Ss)* 180/np.pi
        elevation = 90- zenith
        LGDF.loc[len(LGDF)] = [row["Satelite number"],row["time"],xyzLG, Ss, Sh, azimuth,zenith,elevation]
    return LGDF

LGDFgps = angles(cartesianGPS, recieverPos0)
LGDFBeiDou = angles(cartesianBeiDou, recieverPos0)
LGDFGalileo = angles(cartesianGalileo, recieverPos0)
LGDFGLONASS = angles(cartesianGLONASS, recieverPos0)
LGDFNavIC = angles(cartesianNavIC, recieverPos0)
LGDFQZSS = angles(cartesianQZSS, recieverPos0)
LGDFSBAS = angles(cartesianSBAS, recieverPos0)


filtered_data = LGDFQZSS[LGDFQZSS["Satelite number"] == "J02"]

plt.figure(figsize=(10,10))
plt.plot(filtered_data["time"], filtered_data["elevation"], label = "QZSS")
plt.xlabel("Time")
plt.ylabel("Elevation")
plt.title("Elevation vs Time for Satellite G01")
plt.legend()
plt.show()







