import os
from flask import Flask, request, render_template
from twilio.util import TwilioCapability
from credentials import account_sid, auth_token, application_sid

app = Flask(__name__)
app.config['DEBUG'] = True

def generate_token():
    capability = TwilioCapability(account_sid, auth_token)
    capability.allow_client_outgoing(application_sid)
    test = capability.generate()
    print(test)
    #return capaddbility.generate()
    return test

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['RecordingUrl']
    r = requests.get(url)
    #process r.content

@app.route('/record', methods=['GET', 'POST'])
def record():
    twilio_token = generate_token() 
    return render_template('record.html', token = twilio_token)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

