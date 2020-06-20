from flask import Flask
from flask import make_response
from flask import jsonify
from flask import request
import logging
import threading


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/opi/events', methods=['POST'])
def get_tasks():

    data = request.json
    event =  data['event']
    entity = data['entity']
    if len(data['pair']) != 2:
        return make_response(jsonify({'error': 'Missing Slice Pair'}), 404)
    if event == "" or entity == "":
        return make_response(jsonify({'error': 'Wrong JSON'}), 404)

    if event == "PATH_CHANGED":
        print("Fazer O NASOR Criar outro Slice via message SLICE_CREATOR")
        return jsonify({'response': 'Forwarded to NASOR'})

def flaskThread(app_name):
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    logging.debug('Running through IDE - OpenPolicyInterface (OPI)')
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    print("OPI Running through Import:")
    x = threading.Thread(target=flaskThread, args=(1,))
    x.start()


