
from flask import Flask, jsonify, request
from flask_cors import CORS
from computebaner import  runData
from computeDOP import best

app = Flask(__name__)

# Globally enable CORS for all routes
CORS(app, resources={r"/satellites": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.before_request
def handle_cors_preflight():
    # Catch and handle preflight requests explicitly
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'Preflight request passed'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

@app.route('/satellites', methods=['POST'])
def satellites():
    # Main POST request handling
    data = request.json  
    time = data.get('time').strip('Z')
    elevation_angle = data.get('elevationAngle')
    gnss = data.get('GNSS')
    epoch = data.get('epoch')
    
    is_processing = True
    list, df = runData(gnss, elevation_angle, time, epoch) 
    DOPvalues = best(df)
    is_processing = False
    
    if not is_processing:
        response = jsonify({'message': 'Data processed successfully', 'data': list, 'DOP': DOPvalues})
        return response, 200
    else:
        response = jsonify({"data": "Data is not ready"})
        return response, 202

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)



