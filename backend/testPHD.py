
import pandas as pd

#runData3(["GPS"], "0", "2023-12-11T10:13:34.000")

import numpy as np
# import h5py
# f = h5py.File('fromPHD/RN05345W1_L12.mat','r')
# data = f.get('')
# data = np.array(data) # For converting to a NumPy array
# f.close()
# print(data)
xyzfile = pd.read_csv("testPHDresults.csv")

# WGS84 ellipsoid constants
a = 6378137.0  # Semi-major axis
e2 = 6.69437999014e-3  # First eccentricity squared

def ecef_to_geodetic(x, y, z):
    b = a * (1 - e2)  # Semi-minor axis
    ep = np.sqrt((a**2 - b**2) / b**2)
    p = np.sqrt(x**2 + y**2)
    theta = np.arctan2(z * a, p * b)
    lon = np.arctan2(y, x)
    lat = np.arctan2(z + ep**2 * b * np.sin(theta)**3, p - e2 * a * np.cos(theta)**3)
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    alt = p / np.cos(lat) - N
    lat = np.degrees(lat)
    lon = np.degrees(lon)
    return lat, lon, alt
def ecef_to_neu(x_sat, y_sat, z_sat, x_rec, y_rec, z_rec):
    # Konverter referansepunkt (mottaker) til LLH
    lat, lon, h = ecef_to_geodetic(x_rec, y_rec, z_rec)
    
    # Konverter til radianer
    lat = np.radians(lat)
    lon = np.radians(lon)
    
    # Rotasjonsmatrise fra ECEF til NEU
    R = np.array([
        [-np.sin(lat)*np.cos(lon), -np.sin(lon), np.cos(lat)*np.cos(lon)],
        [-np.sin(lat)*np.sin(lon), np.cos(lon), np.cos(lat)*np.sin(lon)],
        [np.cos(lat), 0, np.sin(lat)]
    ])
    
    # Beregn differansen mellom satellitt og mottaker i ECEF
    dx = x_sat - x_rec
    dy = y_sat - y_rec
    dz = z_sat - z_rec
    
    # Lag differansevektor
    d = np.array([dx, dy, dz])
    
    # Multipliser rotasjonsmatrisen med differansevektoren for å få NEU
    neu = np.dot(R, d)
    
    return neu[0], neu[1], neu[2]  # Returnerer North, East, Up



# ECEF-koordinater for satellitt og mottaker (bare eksempler)
 # Satellittposisjon i meter
x_rec, y_rec, z_rec = 2815213.6424,   517185.1188 , 5680790.1522  # Mottakerposisjon i meter
with open("testPHDresultsNEU.csv", "w") as file:
    file.write(f"SatelliteNr , TOW, N, E, U\n")
    for index,row in xyzfile.iterrows():
        x_sat, y_sat, z_sat = row["X"], row["Y"], row["Z"]
        # Konverter satellittens posisjon til NEU relativt til mottakeren
        north, east, up = ecef_to_neu(x_sat, y_sat, z_sat, x_rec, y_rec, z_rec)
        file.write(f"{row['Satellitenumber']},{row['TOW']},{north},{east},{up}\n")
        #print(f"North: {north} meters, East: {east} meters, Up: {up} meters")

