

from computebaner import  runData
from computeDOP import best

gnss = ["GPS","GLONASS","BeiDou", "Galileo"]
elevation_angle = "10"
time = "2024-09-25T01:00:00.000"
epoch = "6"
def satellites():
  
    list, df = runData(gnss, elevation_angle, time, epoch) 
    print("doneList")
    DOPvalues = best(df)
    print(DOPvalues)

    # if not is_prosessing:
    #     return jsonify({'message': 'Data processed successfully', 'satellites': LGDF_dict, 'GDOP':GDOP, 'PDOP':PDOP, 'TDOP':TDOP}), 200
    # else:
    #     return jsonify({"data": "Data is not ready"}), 202
satellites()