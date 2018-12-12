from flask import Flask,render_template,request
import jinja2, adal, requests

app = Flask(__name__)
app.debug = True

@app.route('/')
def homepage():

    return render_template('test.html')

@app.route('/', methods=['POST'])
def submit_data():
    try:
        if request.method == 'POST':
            endpoint = request.form.get('endpoint')
        SESSION = requests.Session()
        url = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': "xxxxxxxxxxxxx",
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': "x",
        }

        resp = SESSION.post(url, data=data)
        token = resp.json().get('access_token')
        SESSION.headers.update({'Content-Type': 'application\json', 'Authorization': 'Bearer {}'.format(token)})
        graphdata = SESSION.get(endpoint).json()
        return render_template('test.html', token=token, graphdata=graphdata, endpoint=endpoint)

    except Exception as error:
        print('Caught this error: ' + repr(error))
        return render_template('test.html', token=token, graphdata='Error Invalid Query', endpoint='Error Invalid Query')


if __name__ == '__main__':
    app.run()





