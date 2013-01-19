import os
from flask import Flask
from flask import request
from flask import render_template
from twilio.util import TwilioCapability

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/process', methods=['POST'])
def process():
    url = request.form['RecordingUrl']
    r = requests.get(url)
    #process r.content

@app.route('/record')
def record():
    return render_template('record.html')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

