import requests,json

token_endpoint = "https://login.microsoftonline.com/microsoft.onmicrosoft.com/oauth2/v2.0/token"

data = {
'grant_type': 'client_credentials',
'client_id' :  'Client_ID',
'client_secret' : 'Client_Secret',
'scope' :'https://vault.azure.net/.default'
}

# VAULT_URL must be in the format 'https://<vaultname>.vault.azure.net'
uri = "https://<vaultname>.vault.azure.net/keys/key?api-version=2016-10-01"
uri2 = "https://<vaultname>.vault.azure.net/secrets/secretfrompython?api-version=2016-10-01"
uri3 = "https://<vaultname>.vault.azure.net/keys/keykrassy/create?api-version=2016-10-01"
r = requests.post(token_endpoint,data=data)
token = r.json().get('access_token')

headers = {'Authorization': 'Bearer {}'.format(token)}

key_request2 = requests.get(uri,headers=headers).json()
key_request = requests.get(uri2,headers=headers).json()
key_create = requests.post(uri3,headers=headers)
values = key_request['value']
print(values,'\n',key_request,'\n',key_request2)

"https://uaekeyvault.vault.azure.net/keys/keykrassy?api-version=2016-10-01"