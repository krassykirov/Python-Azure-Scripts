import adal,requests,json

url = 'https://login.microsoftonline.com/<Domain>.onmicrosoft.com/oauth2/v2.0/token'

data = {
    'grant_type': 'client_credentials',
    'client_id' : "APP_ID",
    'client_secret': "APP_SECRET",
    'scope': 'https://graph.microsoft.com/.default'
   }

r = requests.post(url, data=data)
token = r.json().get('access_token')
print(token)

headers =({
    'Authorization': "Bearer {}".format(token),
    'Content-Type' : 'application/json',
 })

payload = json.dumps({"passwordProfile" :{"forceChangePasswordNextSignIn":"false", "password":"P@ssword"}})
uri = "https://graph.microsoft.com/beta/users/USER@DOMAIN.onmicrosoft.com"

r = requests.patch(uri, headers=headers,data=payload )
print(r,r.content)

