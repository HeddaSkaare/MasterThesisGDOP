
import pandas as pd
import numpy as np
import re
import ahrs
from datetime import datetime
from dataframes import structured_dataG, structured_dataR, structured_dataE, structured_dataJ, structured_dataC, structured_dataI, structured_dataS


content = []
with open("BRDC00IGS_R_20242520000_01D_MN.rnx", "r") as file:
    content = file.read()

# G: GPS
# R: GLONASS
# E: Galileo
# J: QZSS
# C: BDS
# I: NavIC/IRNSS
# S: SBAS payload
split_index = content.index("END OF HEADER")
header_part = content[:split_index] # baneinformasjon
data_part = content[split_index+13:] #satelitt informasjon

satellitt_data = re.split(r'(?=[GRJCIS])', data_part)[1:]

data_for_Galileio = []

def split_on_second_sign(s):
    
    signs = [m.start() for m in re.finditer(r'(?<![eE])[+-]', s)]
    
    if not signs:
        return s

    parts = []
    last_index = 0
    for idx in signs:
        parts.append(s[last_index:idx])  
        last_index = idx 
    parts.append(s[last_index:])
    
    return parts

def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            flat_list.extend(item)  # Legg til alle elementer i item
        else:
            flat_list.append(item)  # Hvis ikke, legg til elementet direkte
    return flat_list

def strToFloat(inputstring):
    splittedString = inputstring.split("E")
    num = float(splittedString[0])
    potens = int(splittedString[1])
    return num * 10**potens



def GPSdata(satellitt_id,time, finalTallList, finalSVList):
    
    structured_dataG.loc[len(structured_dataG)]  = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11],
        finalTallList[12],
        finalTallList[13],
        finalTallList[14],
        finalTallList[15],
        finalTallList[16],
        finalTallList[17],
        finalTallList[18],
        finalTallList[19],
        finalTallList[20],
        finalTallList[21],
        finalTallList[22],
        finalTallList[23],
        finalTallList[24],
        finalTallList[25]
    ]

def GLONASSdata(satellitt_id,time, finalTallList, finalSVList):

    structured_dataR.loc[len(structured_dataR)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11]
    ]

def Galileiodata(satellitt_id,time, finalTallList, finalSVList):
    structured_dataE.loc[len(structured_dataE)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11],
        finalTallList[12],
        finalTallList[13],
        finalTallList[14],
        finalTallList[15],
        finalTallList[16],
        finalTallList[17],
        finalTallList[18],
        finalTallList[19],
        finalTallList[20],
        finalTallList[21],
        finalTallList[22],
        finalTallList[23]
    ]

def QZSSdata(satellitt_id,time, finalTallList, finalSVList):
    
    structured_dataJ.loc[len(structured_dataJ)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11],
        finalTallList[12],
        finalTallList[13],
        finalTallList[14],
        finalTallList[15],
        finalTallList[16],
        finalTallList[17],
        finalTallList[18],
        finalTallList[19],
        finalTallList[20],
        finalTallList[21],
        finalTallList[22],
        finalTallList[23],
        finalTallList[24],
        finalTallList[25]
    ]

def BeiDoudata(satellitt_id,time, finalTallList, finalSVList):

    structured_dataC.loc[len(structured_dataC)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11],
        finalTallList[12],
        finalTallList[13],
        finalTallList[14],
        finalTallList[15],
        finalTallList[16],
        finalTallList[17],
        finalTallList[18],
        finalTallList[19],
        finalTallList[20],
        finalTallList[21],
        finalTallList[22],
        finalTallList[23],
        finalTallList[24],
        finalTallList[25]
    ]

def NavICdata(satellitt_id,time, finalTallList, finalSVList):
    structured_dataI.loc[len(structured_dataI)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11],
        finalTallList[12],
        finalTallList[13],
        finalTallList[14],
        finalTallList[15],
        finalTallList[16],
        finalTallList[17],
        finalTallList[18],
        finalTallList[19],
        finalTallList[20],
        finalTallList[21],
        finalTallList[22],
        finalTallList[23],
        finalTallList[24]
    ]

def SBASdata(satellitt_id,time, finalTallList, finalSVList):
    structured_dataS.loc[len(structured_dataS)] = [
        satellitt_id,
        time,
        finalSVList[0],
        finalSVList[1],
        finalSVList[2],
        finalTallList[0],
        finalTallList[1],
        finalTallList[2],
        finalTallList[3],
        finalTallList[4],
        finalTallList[5],
        finalTallList[6],
        finalTallList[7],
        finalTallList[8],
        finalTallList[9],
        finalTallList[10],
        finalTallList[11]
    ]
for i in range(0,len(satellitt_data)):
    lines = satellitt_data[i].strip().splitlines()
    satellitt_id = lines[0].split(' ')[0]  # Første linje inneholder satellitt-ID (f.eks. G08)
    if ("R" in satellitt_id) and (len(lines) >4):
        print("inni")
        Edata = lines[4:]
        lines = lines[:4]
        #data_for_Galileio += [[Edata[i:i + 8]] for i in range(0, len(Edata), 8)]
        for i in range(0, len(Edata), 8):
            data_for_Galileio.append(Edata[i:i + 8])
 
    forsteLinje = lines[0].split()[1:]
    tall = " ".join(lines[1:]).split()  # Kombinerer linjene og splittes på mellomrom
    flattened_forstelinje = flatten(list(map(split_on_second_sign, forsteLinje)))
    flattened_tall = flatten(list(map(split_on_second_sign, tall)))
    cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']

    time = datetime(int(cleaned_forstelinje[0]),int(cleaned_forstelinje[1]), int(cleaned_forstelinje[2]), int(cleaned_forstelinje[3]), int(cleaned_forstelinje[4]), int(cleaned_forstelinje[5]))
    
    SV = cleaned_forstelinje[6:]
    
    cleaned_tall = [item for item in flattened_tall if item != '']
    finalTallList = []
    finalSVList = []
    for value in SV:
        floatNumber = strToFloat(value)
        finalSVList += [floatNumber]
    for value in cleaned_tall:
        floatNumber = strToFloat(value)
        finalTallList += [floatNumber]
    #må llegg einn logikk for etter R at man splitter i E

    if "G" in satellitt_id:
        GPSdata(satellitt_id,time,finalTallList, finalSVList)
    elif "R" in satellitt_id:
        GLONASSdata(satellitt_id,time,finalTallList, finalSVList)
    elif "J" in satellitt_id:
        QZSSdata(satellitt_id,time,finalTallList, finalSVList)
    elif "C" in satellitt_id:
        BeiDoudata(satellitt_id,time,finalTallList, finalSVList)
    elif "I" in satellitt_id:
        NavICdata(satellitt_id,time,finalTallList, finalSVList)
    elif "S" in satellitt_id:
        SBASdata(satellitt_id,time,finalTallList, finalSVList)


for i in range(0,len(data_for_Galileio)):
    lines = data_for_Galileio[i]
    satellitt_id = lines[0].split(' ')[0]  
    forsteLinje = lines[0].split()[1:]
    tall = " ".join(lines[1:]).split()  # Kombinerer linjene og splittes på mellomrom
    flattened_forstelinje = flatten(list(map(split_on_second_sign, forsteLinje)))
    
    flattened_tall = flatten(list(map(split_on_second_sign, tall)))
    cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']

    time = datetime(int(cleaned_forstelinje[0]),int(cleaned_forstelinje[1]), int(cleaned_forstelinje[2]), int(cleaned_forstelinje[3]), int(cleaned_forstelinje[4]), int(cleaned_forstelinje[5]))
    
    SV = cleaned_forstelinje[6:]
    
    cleaned_tall = [item for item in flattened_tall if item != '']
    finalTallList = []
    finalSVList = []
    for value in SV:
        floatNumber = strToFloat(value)
        finalSVList += [floatNumber]
    for value in cleaned_tall:
        floatNumber = strToFloat(value)
        finalTallList += [floatNumber]
    Galileiodata(satellitt_id,time,finalTallList, finalSVList)

print(structured_dataG.head())
print(structured_dataR.head())
print(structured_dataE.head())
print(satellitt_data[len(structured_dataG)+len(structured_dataR)+ len(structured_dataE)])
print(structured_dataC.head())
print(structured_dataJ.head())
print(structured_dataI.head())
print(structured_dataS.head())