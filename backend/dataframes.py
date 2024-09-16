
import pandas as pd

# G: GPS
# R: GLONASS
# E: Galileo
# J: QZSS
# C: BDS
# I: NavIC/IRNSS
# S: SBAS payload

structured_dataG = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "IODE",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Codes on L2 channel",
    "GPS Week",
    "L2 P",
    "SV accurracy",
    "SV health",
    "TGD",
    "IODC",
    "t_tm",
    "Fit Interval"
])
structured_dataR = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "X",
    "Vx",
    "ax",
    "Health",
    "Y",
    "Vy",
    "ay",
    "Frequency number",
    "Z",
    "Vz",
    "az",
    "Age of operation",
])
structured_dataE = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "IODnav",
    "C_rs",
    "Delta n0",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Data source",
    "GAL Week",
    "SISA signal",
    "SV health",
    "BGDa",
    "BGDb",
    "t_tm"
])
structured_dataJ = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "IODE",
    "C_rs",
    "Delta n",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Codes on L2 channel",
    "GPS Week",
    "L2P",
    "SV accurracy",
    "SV health",
    "TGD",
    "IODC",
    "t_tm",
    "Fit Interval"
])
structured_dataC = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "AODE",
    "C_rs",
    "Delta n",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Spare1",
    "BDT Week",
    "Spare2",
    "SV accurracy",
    "SatH1",
    "TGD1",
    "TGD2",
    "t_tm",
    "AODC"
])

structured_dataI = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "IODEC",
    "C_rs",
    "Delta n",
    "M0",
    "C_uc",
    "e",
    "C_us",
    "sqrt(A)",
    "T_oe",
    "C_ic",
    "OMEGA0",
    "C_is",
    "i0",
    "C_rc",
    "omega",
    "OMEGA DOT",
    "IDOT",
    "Spare1",
    "IRN Week",
    "Spare2",
    "User Range accurracy",
    "Health",
    "TGD",
    "Spare3",
    "t_tm"
])

structured_dataS = pd.DataFrame(columns = [
    "satelite_id",
    "Datetime",
    "a0",
    "a1",
    "a2",
    "X",
    "Vx",
    "ax",
    "Health",
    "Y",
    "Vy",
    "ay",
    "Accurracy code",
    "Z",
    "Vz",
    "az",
    "IODN"
])