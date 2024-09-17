from flask import Flask, jsonify
from computebaner import LGDFgps
from sortData import satellitt_data
# from flask_cors import CORS
# CORS(app)

app = Flask(__name__)

@app.route('/api/get_value', methods=['GET'])
def get_value():
    # Her kan du kjøre modellen din og hente verdier
    model_output = {"value": LGDFgps}
    return jsonify(model_output)

if __name__ == '__main__':
    app.run(debug=True)