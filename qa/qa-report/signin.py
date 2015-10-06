#!/usr/bin/python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Percolata QA bug report system"""

__author__ = 'zhixin@percolata.com'

import json
import random
import string
from apiclient.discovery import build
from apiclient import errors

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import send_file
from flask import session

import httplib2
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

import oauth2 as oauth
import requests
import urllib
import re
import certifi

APPLICATION_NAME = 'Percolata Bug Report'
SCOPES = ['email','profile']

BITBUCKET_KEY = "rg5hHG4uxr2nTbJaMG"
BITBUCKET_SECRET = "kq7mnZsVdVfRyzKwZkbWZGcQaFkVLZW2"
# Request token URL for BitBucket.
bb_request_token_url = "https://bitbucket.org/api/1.0/oauth/request_token"
#access_token_url = 'https://bitbucket.org/api/1.0/oauth/access_token'
#authorization_url = 'https://bitbucket.org/api/1.0/oauth/authenticate'
bb_issue_request_url = 'https://bitbucket.org/api/1.0/repositories/percolata/qa/issues/'

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for x in xrange(32))


# See the simplekv documentation for details
store = DictStore()


# This will replace the app's session handling
KVSessionExtension(store, app)


# Update client_secrets.json with your Google API project information.
# Do not change this assignment.
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
SERVICE = build(serviceName='oauth2', version='v2')

class NoUserIdException(Exception):
  """Error raised when no user ID could be retrieved."""

@app.route('/', methods=['GET'])
def index():
  """Initialize a session for the current user, and render index.html."""
  # Create a state token to prevent request forgery.
  # Store it in the session for later validation.
  state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for x in xrange(32))
  session['state'] = state
  # Set the Client ID, Token State, and Application Name in the HTML while
  # serving it.
  print state, CLIENT_ID
  response = make_response(
      render_template('index.html',
                      CLIENT_ID=CLIENT_ID,
                      STATE=state,
                      APPLICATION_NAME=APPLICATION_NAME))
  response.headers['Content-Type'] = 'text/html'
  return response

@app.route('/signin_button.png', methods=['GET'])
def signin_button():
  """Returns the button image for sign-in."""
  return send_file("templates/signin_button.png", mimetype='image/gif')

@app.route('/page-loader.gif', methods=['GET'])
def page_loader():
  """Returns the page loader image for ajax."""
  return send_file("templates/page-loader.gif", mimetype='image/gif')

@app.route('/connect', methods=['POST'])
def connect():
  """Exchange the one-time authorization code for a token and
  store the token in the session."""
  # Ensure that the request is not a forgery and that the user sending
  # this connect request is the expected user.
  if request.args.get('state', '') != session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Normally, the state is a one-time token; however, in this example,
  # we want the user to be able to connect and disconnect
  # without reloading the page.  Thus, for demonstration, we don't
  # implement this best practice.
  # del session['state']

  code = request.data

  try:
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope=' '.join(SCOPES))
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(
        json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    print 'An error occurred: %s' % e
  authorized_user = False
  if user_info and user_info.get('email'):
    user_domain = user_info.get('email')
    if "baysensors" in user_domain or "percolata" in user_domain:
      authorized_user = True
  else:
    raise NoUserIdException()
  print "authorized_user is: "+str(authorized_user)
  # An ID Token is a cryptographically-signed JSON object encoded in base 64.
  # Normally, it is critical that you validate an ID Token before you use it,
  # but since you are communicating directly with Google over an
  # intermediary-free HTTPS channel and using your Client Secret to
  # authenticate yourself to Google, you can be confident that the token you
  # receive really comes from Google and is valid. If your server passes the
  # ID Token to other components of your app, it is extremely important that
  # the other components validate the token before using it.
  if not authorized_user:
    response = make_response(json.dumps('Unauthorized user', 401))
    response.headers['Content-Type'] = 'application/json'
    return response

  gplus_id = credentials.id_token['sub']

  stored_credentials = session.get('credentials')
  stored_gplus_id = session.get('gplus_id')
  if stored_credentials is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps('Current user is already connected.'),
                             200)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Store the access token in the session for later use.
  session['credentials'] = credentials
  session['gplus_id'] = gplus_id
  response = make_response(json.dumps('Successfully connected user.', 200))
  response.headers['Content-Type'] = 'application/json'
  return response


@app.route('/disconnect', methods=['POST'])
def disconnect():
  """Revoke current user's token and reset their session."""

  # Only disconnect a connected user.
  credentials = session.get('credentials')
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Execute HTTP GET request to revoke current token.
  access_token = credentials.access_token
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]

  if result['status'] == '200':
    # Reset the user's session.
    del session['credentials']
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
  else:
    # For whatever reason, the given token was invalid.
    response = make_response(
        json.dumps('Failed to revoke token for given user.', 400))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/buglist', methods=['GET'])
def buglist():
  """Get list of buglist."""
  credentials = session.get('credentials')
  if credentials is None:
    response = make_response(json.dumps('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  try:
    # parse the buglist contents to the html
    buglist_json = get_buglist()
    response = make_response(json.dumps(buglist_json), 200)
    response.headers['Content-Type'] = 'application/json'
    print response
    return response
  except AccessTokenRefreshError:
    response = make_response(json.dumps('Failed to refresh access token.'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

def get_buglist():
  # Create your consumer with the proper key/secret.
  consumer = oauth.Consumer(key=BITBUCKET_KEY, secret=BITBUCKET_SECRET)


  # Create our client.
  client = oauth.Client(consumer)
  client.ca_certs = certifi.where()
  # The OAuth Client request works just like httplib2 for the most part.
  #resp, content = client.request(bb_request_token_url, "POST", 
  #  body=urllib.urlencode({'oauth_callback':"http%3A%2F%coolapp.local%2Fauth.php,bitbucketclient%3A%2F%2Fcallback"}))
  #print content

  #parse_token = re.match(r'oauth_token_secret=(.*)&oauth_token=(.*)&oauth_callback_confirmed=(.*)', content)
  #oauth_token_secret = parse_token.group(1)
  #oauth_token = parse_token.group(2)
  #oauth_confirmed = parse_token.group(3)

  resp, content = client.request(bb_issue_request_url, "GET", 
    body=urllib.urlencode({'oauth_consumer_key':BITBUCKET_KEY}))
  #print content
  content = json.loads(content)
  bugdata = []
  # for item in content['issues']:
  #   bugdata.append({'id':item['local_id'],
  #     'component':item['metadata']['component'],
  #     'status':item['status'],
  #     'priority':item['priority'],
  #     'kind':item['metadata']['kind'],
  #     'milestone':item['metadata']['milestone'],
  #     'content':item['content'],
  #     'reported_by':item['reported_by']['display_name'],
  #     'assigned_to':item['responsible']['display_name'],
  #     'utc_created_on':item['utc_created_on'],
  #     'utc_last_updated':item['utc_last_updated'],
  #     'version':item['metadata']['version']
  #     })
  #   print bugdata
  nBug = content['count']
  for i in range(nBug):
    resp, bug = client.request(bb_issue_request_url+str(i+1), "GET", 
      body=urllib.urlencode({'oauth_consumer_key':BITBUCKET_KEY}))
    item = json.loads(bug)
    bugdata.append({'id':item['local_id'],
    'component':item['metadata']['component'],
    'status':item['status'],
    'priority':item['priority'],
    'kind':item['metadata']['kind'],
    'milestone':item['metadata']['milestone'],
    'title':item['title'],
    'reported_by':item['reported_by']['display_name'],
    'assigned_to':item['responsible']['display_name'],
    'utc_created_on':item['utc_created_on'],
    'utc_last_updated':item['utc_last_updated'],
    'version':item['metadata']['version']
    })
  print len(bugdata)
  return bugdata

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=80)
