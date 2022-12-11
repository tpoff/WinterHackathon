# ****************** Execution Setup **********************
# $ export FLASK_APP=FlaskApp
# $ export FLASK_ENV=development
# $ flask run
#
# http://127.0.0.1:5000/api/status
# *********************************************************

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Hackathon!'

@app.route('/api/test')
def api_test():
    return jsonify({'name': 'Dallas',
                    'email': 'Dallas@outlook.com'}
                  )
    
@app.route('/api/status')
def api_status():
  return "status"