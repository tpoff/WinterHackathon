# ****************** Execution Setup **********************
# $ export FLASK_APP=FlaskApp
# $ export FLASK_ENV=development
# $ flask run
#
# http://127.0.0.1:5000/api/status
# *********************************************************

from flask import Flask, jsonify
from Bot_Process import Bot_Process
from Text_To_Speech.Text_To_Speech import Text_To_Speech_Local_Wav_Output, Text_To_Speech_Uberduck_Wav_Output

app = Flask(__name__)

proc = Bot_Process()

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
  global proc
  
  return proc.to_dict()


if __name__ == "__main__":
    proc.start()
    app.run(threaded=True)