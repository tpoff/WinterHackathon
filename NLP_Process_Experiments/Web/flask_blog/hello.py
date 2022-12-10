from flask import Flask, request, escape, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/greet')
def greet():
    name = request.args['name']
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Greeting</title>
    </head>
    <body>
        <h1>Hi {}</h1>
    </body>
    </html>'''.format(escape(name))

@app.route('/api/test')
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'
                    })