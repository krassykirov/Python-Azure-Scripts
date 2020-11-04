import requests,json

token_endpoint = "https://login.microsoftonline.com/yourdomain.onmicrosoft.com/oauth2/v2.0/token"

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

###############################################################
###############################################################
###############################################################

from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials

credentials = ServicePrincipalCredentials(
        client_id = 'YourClientAdd',
        secret = 'YourSecret',
        tenant = 'domain.onmicrosoft.com',
    )
VAULT_URL = 'https://YourKeyvaultNAME.vault.azure.net'
SECRET_ID = 'mysecret'
client = KeyVaultClient(credentials)
# VAULT_URL must be in the format 'https://<vaultname>.vault.azure.net'
# SECRET_VERSION is required, and can be obtained with the KeyVaultClient.get_secret_versions(self, vault_url, secret_id) API
key_bundle = client.get_key(VAULT_URL,'key' , 'e371b887e1f54708a947cc8570272543')
key = key_bundle.key
secret_bundle = client.get_secret(VAULT_URL, SECRET_ID, '90cdeb79bc494b77920ed2bbdba8139e')
#Create a Secret
my_secret = client.set_secret(VAULT_URL, "secretfrompython2", "pythonvalue2")
#Create a Key
key2 = client.create_key(VAULT_URL, "key2","RSA")
versions = client.get_key_versions(VAULT_URL, SECRET_ID)
#Delete a Key delete_key(vault_base_url, key_name, custom_headers=None, raw=False, **operation_config)
#client.delete_key(VAULT_URL,"key2")
print(my_secret)
print(secret_bundle)
print(key)
print(key2)
