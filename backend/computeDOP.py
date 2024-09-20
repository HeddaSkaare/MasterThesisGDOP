
import itertools
import numpy as np
from computebaner import recieverPos0

T = 558000
GM = 3.986005*10**14
we = 7.2921151467 *10**(-5) 
c = 299792458
def geometric_range(sat_pos, rec_pos):
    return np.sqrt((sat_pos[2] - rec_pos[0])**2 +
                   (sat_pos[3] - rec_pos[1])**2 +
                   (sat_pos[4] - rec_pos[2])**2)


def DOPvalues(satellites, recieverPos0):
    A = np.zeros((7, 4))  
    Qxx =np.zeros((4, 4)) 
    #creates the A matrix
    i = 0
    for satellite in satellites:
        rho_i = geometric_range(satellite, recieverPos0)
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
    satellites_array = []
    for satellite in satellites:
        for i in range(0,len(satellite)-1):
            satellites_array += [satellite.loc[i]["Satelitenumber"], satellite.loc[i]["time"], satellite.loc[i]["X"], satellite.loc[i]["Y"], satellite.loc[i]["Z"]]
    best_GDOP = float('inf') 
    best_subset = None
    # for subset in itertools.combinations(satellites_array, 7):
    #     print("hei")
    #     GDOP, PDOP, TDOP = DOPvalues(subset, recieverPos0)
        
    #     # Find the subset with the lowest GDOP
    #     if GDOP < best_GDOP:
    #         print("hei2")
    #         best_GDOP = GDOP
    #         best_subset = subset
    for subset in itertools.combinations(satellites_array, 7):
        print("hei")
        GDOP, PDOP, TDOP = DOPvalues(subset, recieverPos0)
        
        # Find the subset with the lowest GDOP
        if GDOP < best_GDOP:
            print("hei2")
            best_GDOP = GDOP
            best_subset = subset
    
    return best_GDOP, best_subset