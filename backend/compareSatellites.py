import pandas as pd
import datetime


def loadSat(day,time,pnr):
    df = pd.read_csv(f'backend/DataFrames/{day}/structured_data{pnr[0]}.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index(['satelite_id','Datetime'],inplace=True)
    print(df.loc[pnr, time])
    return df.loc[pnr, time]

#time = datetime.datetime(2024,10,13,00,00)

#loadSat(290,'2024-10-15 23:45:00','R01')

