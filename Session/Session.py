from flask import Flask,render_template,request
import jinja2, adal, requests

app = Flask(__name__)
app.debug = True

SESSION = requests.Session()

@app.route('/')
def homepage():

    return render_template('test.html')

@app.route('/', methods=['POST'])
def submit_data():
    try:
        if request.method == 'POST':
            endpoint = request.form.get('endpoint')
        url = 'https://login.microsoftonline.com/sg77.onmicrosoft.com/oauth2/v2.0/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': "9a99e41c-b2d7-40bf-bd39-7531b9d04cdf",
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': "G3H4FBAKm6ORNJJi8HHid9nD5tsBsTkGA8/uOb+DcVY=",
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





