from credentials import account_sid, auth_token, application_sid, client_id, client_secret, client_token, client_id, client_secret
from flask import Flask, request, render_template, redirect
from twilio.util import TwilioCapability
from urllib     import urlopen 
from xml.dom    import minidom
from random     import random
from time       import sleep
import twilio.twiml
from flask.ext.sqlalchemy import SQLAlchemy
import sox
import os
import requests
import soundcloud

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

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

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    return render_template('filter.html')

@app.route('/recordtwilio', methods=['GET', 'POST'])
def recordtwilio():
    resp = twilio.twiml.Response()
    resp.record(maxLength="30", action="/handle-recording")
    return str(resp)

@app.route('/handle-recording', methods=['GET', 'POST'])
def handle_recording():
    url = request.form['RecordingUrl']
    r = requests.get(url)

    random_id = int(random() * 10**6)
    with open('/tmp/' + str(random_id) + '_original.wav','wb') as f:
        f.write( r.content )
    upload( random_id )                         # uploading original

    audio_effects = sox.do_all( random_id )     # creating filtered audio
    for effect in audio_effects:
        upload( random_id, effect )
        sleep(1)

    return """  
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
    </Response>
    """

@app.route('/record', methods=['GET', 'POST'])
def record():
    twilio_token = generate_token() 
    return render_template('record.html', token = twilio_token)

@app.route('/login')
def login():
    # create client object with app credentials
    client = soundcloud.Client(client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri='http://localhost:5000/token')
    # redirect user to authorize URL
    return redirect(client.authorize_url())

@app.route('/token')
def token():
    # create client object with app credentials
    client = soundcloud.Client(client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri='http://localhost:5000/token')
    code = request.args.get('code', '')
    access_token = client.exchange_token(code)
    return 'hey bro: ' + access_token.access_token + 'lol'

def upload(random_id, process = 'original'):
    # create client object with access token
    client = soundcloud.Client(access_token=client_token)
    track_path = '/tmp/' + str(random_id) + '_' + process + '.wav'
    # upload audio file
    with open(track_path,'rb') as track:
        with open('assets/img/ban.jpeg','rb') as banana:
            track = client.post('/tracks', track={
                'title': 'Upload #: {}-{}'.format(random_id,process),
                'asset_data': track,
                'artwork_data': banana
            })  
    # print track link
    return track.permalink_url

def widget(track_url):
    client = soundcloud.Client(access_token=client_token)
    widget = requests.post('http://www.soundcloud.com/oembed', params={'url':track_url})
    new_page = requests.get(widget.url)
    xmldoc = minidom.parse(urlopen(widget.url))
    return xmldoc.getElementsByTagName("html")[0].firstChild.wholeText

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
