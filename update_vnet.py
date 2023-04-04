import requests
from azure.common.credentials import ServicePrincipalCredentials


def update_vnet(vnet_name: str):
    client_id = ""
    tenant_id = ""
    client_secret = ""
    subscription_id = ""
    endpoint = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/{vnet_name}?api-version=2022-09-01"
    cred = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
    token = cred.token.get('access_token')
    headers = {'Authorization': 'Bearer {}'.format(token)}
 
    payload = {
    "properties": {
        "addressSpace": {
        "addressPrefixes": [
            "10.10.10.0/24"
        ]
        }
    },
    "location": "northeurope"
    }
    response = requests.put(endpoint, headers=headers, json=payload)
    print('response:', response.text)
