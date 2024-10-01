

from flask import Flask, jsonify, request
from computebaner import  runData
from computeDOP import best
import logging
from flask_cors import CORS

# Set up basic configuration for logging
#logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
#CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.route('/satellites', methods=['POST', 'OPTIONS'])
def satellites():
    if request.method == 'OPTIONS':
        # Return 200 for the preflight check
        return '', 200
    data = request.json  
    time = data.get('time').strip('Z')
    elevation_angle = data.get('elevationAngle')
    gnss = data.get('GNSS')
    epoch = data.get('epoch')
    
    is_prosessing = True
    list, df = runData(gnss, elevation_angle, time, epoch) 
    DOPvalues = best(df)
    is_prosessing = False

    if not is_prosessing:
        return jsonify({'message': 'Data processed successfully', 'satellites': list, 'DOP':DOPvalues}), 200
    else:
        return jsonify({"data": "Data is not ready"}), 202

@app.route('/initialize', methods=['GET'])
def initialize():
    newData, newDataDf = runData(["GPS","GLONASS","BeiDou", "Galileo", "NavIC", "SBAS"], "10", "2024-09-25T01:00:00.000")
    GDOP, PDOP,TDOP = best(newDataDf)
    return jsonify({'data': newData, 'GDOP':GDOP,'PDOP':PDOP,'TDOP':TDOP }), 200


@app.route('/submit-filter', methods=['POST'])
def submit_time():
    data = request.json  
    start_time = data.get('startTime')
    end_time = data.get('endTime')
    elevation_angle = data.get('elevationAngle')
    gnss = data.get('GNSS')
    stored_data = runData(gnss, elevation_angle, start_time, end_time)  # Long-running function
    return jsonify({'message': 'Data received successfully'}), 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)