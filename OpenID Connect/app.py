import os
import urllib.parse
import uuid
import flask
from flask import Flask,render_template,request,session,flash,url_for
import jinja2, adal, requests

APP = flask.Flask(__name__,template_folder='static/templates')
APP.debug = True
APP.secret_key = 'development'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # enable non-HTTPS for testing

CLIENT_ID = 'Your CLIENT/APP ID '
CLIENT_SECRET = "Your CLIENT SECRET"
REDIRECT_URI = 'http://localhost:5000/login/authorized'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'beta'
SCOPES = ['User.Read'] # Add other scopes/permissions as needed.

SESSION = requests.Session()

@APP.route('/')
def homepage():
        """Render the home page."""
        flask.session.clear()
        SESSION.auth_state = None
        return flask.render_template('homepage.html', sample='ADAL')

@APP.route('/login',methods=['GET', 'POST'])
def login():
        """Prompt user to authenticate."""
        flask.session.clear()
        auth_state = str(uuid.uuid4())
        SESSION.auth_state = auth_state
        prompt_behavior = 'select_account' #prompt_behavior = 'login'
        params = urllib.parse.urlencode({'response_type': 'code id_token',
                                         'client_id': CLIENT_ID,
                                         'redirect_uri': REDIRECT_URI,
                                         'state' : auth_state,
                                         'nonce': str(uuid.uuid4()),
                                         'scope': 'openid email',
                                         'prompt': prompt_behavior,
                                         'response_mode' : 'form_post'})


        return flask.redirect(AUTHORITY_URL + '/oauth2/authorize?' + params)


@APP.route('/login/authorized',methods=['GET', 'POST'])
def authorized():
            #Handler for the application's Redirect Uri. Gets the authorization code from the flask response form dictionary.
            code = request.form.get('code')
            id_token = request.form.get('id_token')
            flask.session['id_token'] = id_token

            auth_state = request.form.get('state')
            if auth_state != SESSION.auth_state:
                print('state returned to redirect URL does not match!')
                SESSION.auth_state = None
                flask.session.clear()
                return flask.redirect(url_for('/'))

            auth_context = adal.AuthenticationContext(AUTHORITY_URL, api_version=None)

            token_response = auth_context.acquire_token_with_authorization_code(
                code, REDIRECT_URI, RESOURCE, CLIENT_ID, CLIENT_SECRET)

            flask.session['access_token'] = token_response['accessToken']

            SESSION.headers.update({'Authorization': f"Bearer {token_response['accessToken']}",
                                    'User-Agent': 'adal-sample',
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json',
                                    'SdkVersion': 'sample-python-adal',
                                    'return-client-request-id': 'true'})

            #print('id_token: {0},"\n", token_response: {1}'.format(id_token,token_response))
           
            return flask.redirect('/graphcall')

@APP.route('/graphcall')
def graphcall():
        """Confirm user authentication by calling Graph and displaying some data."""
        #session contains the id_token+access_token 
        if 'id_token' not in flask.session or 'access_token' not in flask.session:
            SESSION.auth_state = None
            flask.session.clear()
            return flask.redirect(flask.url_for('/'))

        endpoint = RESOURCE + API_VERSION + '/me'
        http_headers = {'client-request-id': str(uuid.uuid4())}
        graphdata = SESSION.get(endpoint, headers=http_headers, stream=False).json()

        return flask.render_template('graphcall.html',
                                     graphdata=graphdata,
                                     endpoint=endpoint,
                                     sample='ADAL',
                                     id_token=flask.session['id_token'],
                                     access_token=flask.session['access_token'])


if __name__ == '__main__':
        APP.run()
        

