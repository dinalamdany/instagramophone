from credentials import account_sid, auth_token, application_sid#, client_token, client_id, client_secret
from flask import Flask, request, render_template, redirect
from twilio.util import TwilioCapability
from urllib import urlopen 
from xml.dom import minidom
from random import random
from sox import do_all
from time import sleep
import os
import requests
import soundcloud


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

    random_id = int(random()*10**6)
    with open('/tmp/' + str(random_id) + '.wav','wb') as f:
        f.write( r.content )
    audio_effects = do_all( random_id ) 
    audio_change = ['reverse','short_echo','long_echo','fast','slow','glacial']
    for i in range(len(audio_effects)):
        upload( '/tmp/' + str(random_id) + '_' + audio_effects[i] + '.wav',
            random_id, audio_change[i])
        sleep(1)

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

def upload(track_path,random_id,process='original'):
    # create client object with access token
    client = soundcloud.Client(access_token=client_token)

    # upload audio file
    track = client.post('/tracks', track={
        'title': 'Upload #: {} Track: {}'.format(random_id,process),
        'asset_data': open(track_path, 'rb'),
        'artwork_data': open('ban.jpeg', 'rb')
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
