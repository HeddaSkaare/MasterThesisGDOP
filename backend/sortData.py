
import math
import pandas as pd
import numpy as np
import re
import ahrs
from datetime import datetime
from dataframes import structured_dataG, structured_dataR, structured_dataE, structured_dataJ, structured_dataC, structured_dataI, structured_dataS
import os
import gzip
import shutil

# G: GPS
# R: GLONASS
# E: Galileo
# J: QZSS
# C: BDS
# I: NavIC/IRNSS
# S: SBAS payload


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
            flat_list.extend(item)  
        else:
            flat_list.append(item) 
    return flat_list

def strToFloat(inputstring):
    splittedString = inputstring.split("E")
    num = float(splittedString[0])
    potens = int(splittedString[1])
    return num * 10**potens



def GPSdata(satellitt_id,time, values_list, SV):
    structured_dataG.loc[len(structured_dataG)]  = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[19],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24],
        values_list[25]
    ]

def GLONASSdata(satellitt_id,time, values_list, SV):
    structured_dataR.loc[len(structured_dataR)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11]
    ]

def Galileiodata(satellitt_id,time, values_list, SV):
    structured_dataE.loc[len(structured_dataE)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24]
    ]

def QZSSdata(satellitt_id,time, values_list, SV):
    
    structured_dataJ.loc[len(structured_dataJ)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[19],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24],
        values_list[25]
    ]

def BeiDoudata(satellitt_id,time, values_list, SV):

    structured_dataC.loc[len(structured_dataC)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[19],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24],
        values_list[25]
    ]

def NavICdata(satellitt_id,time, values_list, SV):
    structured_dataI.loc[len(structured_dataI)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11],
        values_list[12],
        values_list[13],
        values_list[14],
        values_list[15],
        values_list[16],
        values_list[17],
        values_list[18],
        values_list[19],
        values_list[20],
        values_list[21],
        values_list[22],
        values_list[23],
        values_list[24]
    ]

def SBASdata(satellitt_id,time, values_list, SV):
    structured_dataS.loc[len(structured_dataS)] = [
        satellitt_id,
        time,
        SV[0],
        SV[1],
        SV[2],
        values_list[0],
        values_list[1],
        values_list[2],
        values_list[3],
        values_list[4],
        values_list[5],
        values_list[6],
        values_list[7],
        values_list[8],
        values_list[9],
        values_list[10],
        values_list[11]
    ]

def sortData(daynumber):
    if os.path.exists("DataFrames/"+ daynumber+"/structured_dataG.csv"):
        return
    else:
        folderCDDIS = "CDDIS/"
        folderUnzipped = "unzipped/"
        filename = "BRDC00IGS_R_2024"+ daynumber+"0000_01D_MN.rnx.gz"
        

        unzipped_filename = filename[:-3]  # Remove '.gz' from filename
        with gzip.open(folderCDDIS+filename, 'rb') as f_in:
            with open(folderUnzipped+unzipped_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        content = []
        with open(folderUnzipped+unzipped_filename, "r") as file:
            content = file.read()

        split_index = content.index("END OF HEADER")
        header_part = content[:split_index] # baneinformasjon
        data_part = content[split_index+13:] #satelitt informasjon

        satellitt_data = re.split(r'(?=[GRJCIS])', data_part)[1:]
        data_for_Galileio = []
        for i in range(0,len(satellitt_data)):
            lines = satellitt_data[i].strip().splitlines()
            satellitt_id = lines[0].split(' ')[0]  # Første linje inneholder satellitt-ID (f.eks. G08)
            if ("R" in satellitt_id) and (len(lines) >4):
                Edata = lines[4:]
                lines = lines[:4]
                #data_for_Galileio += [[Edata[i:i + 8]] for i in range(0, len(Edata), 8)]
                for i in range(0, len(Edata), 8):
                    data_for_Galileio.append(Edata[i:i + 8])
        
            forsteLinje = lines[0].split()[1:]
            values_lines = lines[1:]

            flattened_forstelinje = flatten(list(map(split_on_second_sign, forsteLinje)))

            cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']
            values_list = []
            for line in values_lines:
                flattenedLine = flatten(list(map(split_on_second_sign, line.split())))
                cleanedLine = [item for item in flattenedLine if item != '']
                while len(cleanedLine)<4:
                    cleanedLine.append(np.nan)
                values_list += cleanedLine

            time = datetime(int(cleaned_forstelinje[0]),int(cleaned_forstelinje[1]), int(cleaned_forstelinje[2]), int(cleaned_forstelinje[3]), int(cleaned_forstelinje[4]), int(cleaned_forstelinje[5]))
            #output_folder = cleaned_forstelinje[0] +'-'+ cleaned_forstelinje[1] +'-'+ cleaned_forstelinje[2]
            SV = cleaned_forstelinje[6:]

            for i in range(len(SV)):
                value = SV[i]
                floatNumber = strToFloat(value)
                SV[i] = floatNumber
            for j in range(len(values_list)):
                value = values_list[j]
                if isinstance(value, str):
                    floatNumber = strToFloat(value)
                    values_list[j] = floatNumber

            if "G" in satellitt_id:
                GPSdata(satellitt_id,time,values_list, SV)
            elif "R" in satellitt_id:
                GLONASSdata(satellitt_id,time,values_list, SV)
            elif "J" in satellitt_id:
                QZSSdata(satellitt_id,time,values_list, SV)
            elif "C" in satellitt_id:
                BeiDoudata(satellitt_id,time,values_list, SV)
            elif "I" in satellitt_id:
                NavICdata(satellitt_id,time,values_list, SV)
            elif "S" in satellitt_id:
                SBASdata(satellitt_id,time,values_list, SV)


        for i in range(0,len(data_for_Galileio)):
            lines = data_for_Galileio[i]
            satellitt_id = lines[0].split(' ')[0]  
            forsteLinje = lines[0].split()[1:]
            values_lines = lines[1:]

            flattened_forstelinje = flatten(list(map(split_on_second_sign, forsteLinje)))

            cleaned_forstelinje = [item for item in flattened_forstelinje if item != '']
            values_list = []
            for line in values_lines:
                flattenedLine = flatten(list(map(split_on_second_sign, line.split())))
                cleanedLine = [item for item in flattenedLine if item != '']
                while len(cleanedLine)<4:
                    cleanedLine.append(np.nan)
                values_list += cleanedLine

            time = datetime(int(cleaned_forstelinje[0]),int(cleaned_forstelinje[1]), int(cleaned_forstelinje[2]), int(cleaned_forstelinje[3]), int(cleaned_forstelinje[4]), int(cleaned_forstelinje[5]))
            
            SV = cleaned_forstelinje[6:]

            for i in range(len(SV)):
                value = SV[i]
                floatNumber = strToFloat(value)
                SV[i] = floatNumber
            for j in range(len(values_list)):
                value = values_list[j]
                if isinstance(value, str):
                    floatNumber = strToFloat(value)
                    values_list[j] = floatNumber

            Galileiodata(satellitt_id,time,values_list, SV)

        output_folder = "DataFrames/"+daynumber
        os.makedirs(output_folder, exist_ok=True)
        file_pathG = os.path.join("DataFrames",daynumber, "structured_dataG.csv")
        structured_dataG.to_csv(file_pathG, index=False)
        file_pathR = os.path.join("DataFrames",daynumber, "structured_dataR.csv")
        structured_dataR.to_csv(file_pathR, index=False)
        file_pathE = os.path.join( "DataFrames",daynumber, "structured_dataE.csv")
        structured_dataE.to_csv(file_pathE, index=False)
        file_pathJ = os.path.join("DataFrames", daynumber, "structured_dataJ.csv")
        structured_dataJ.to_csv(file_pathJ, index=False)
        file_pathC = os.path.join("DataFrames", daynumber, "structured_dataC.csv")
        structured_dataC.to_csv(file_pathC, index=False)
        file_pathI = os.path.join( "DataFrames",daynumber, "structured_dataI.csv")
        structured_dataI.to_csv(file_pathI, index=False)
        file_pathS = os.path.join("DataFrames",daynumber, "structured_dataS.csv")
        structured_dataS.to_csv(file_pathS, index=False)

