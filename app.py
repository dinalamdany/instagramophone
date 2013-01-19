import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import requests
from urllib import urlopen 
from xml.dom import minidom
from twilio.util import TwilioCapability
import soundcloud

atoken = '1-31322-33373233-661cb3c2f871ad2'
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
