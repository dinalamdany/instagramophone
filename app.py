from credentials import account_sid, auth_token, application_sid
from flask import Flask, request, render_template, redirect
from twilio.util import TwilioCapability
from urllib import urlopen 
from xml.dom import minidom

import os
import requests
import soundcloud

atoken = '1-31322-33373233-661cb3c2f871ad2'
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

@app.route('/login')
def login():
    # create client object with app credentials
    client = soundcloud.Client(client_id='a13d2648f3eb94cdea7b54b91bf66762',
                           client_secret='0f6ba718694ea7c2885a085d6d0827d7',
                           redirect_uri='http://localhost:5000/token')

    # redirect user to authorize URL
    return redirect(client.authorize_url())

@app.route('/token')
def token():
    # create client object with app credentials
    client = soundcloud.Client(client_id='a13d2648f3eb94cdea7b54b91bf66762',
                           client_secret='0f6ba718694ea7c2885a085d6d0827d7',
                           redirect_uri='http://localhost:5000/token')
    code = request.args.get('code', '')
    access_token = client.exchange_token(code)
    return 'hey bro: ' + access_token.access_token + 'lol'

def upload(track_path):
    # create client object with access token
    client = soundcloud.Client(access_token=atoken)

    # upload audio file
    track = client.post('/tracks', track={
        'title': 'This is my sound',
        'asset_data': open(track_path, 'rb'),
        'artwork_data': open('ban.jpeg', 'rb')
    }) 

    # print track link
    return track.permalink_url

@app.route('/widget')
def widget(track_url):
    client = soundcloud.Client(access_token=atoken)
    widget = requests.post('http://www.soundcloud.com/oembed', params={'url':track_url})
    new_page = requests.get(widget.url)
    xmldoc = minidom.parse(urlopen(widget.url))
    return xmldoc.getElementsByTagName("html")[0].firstChild.wholeText

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
