""" Send Email with attachement using Client Credentials flow """
""" Need to change client_id, client_secret, User and TENANT """ 

from msrestazure.azure_active_directory import AADTokenCredentials
import adal,requests,os,base64

authority_host_uri = 'https://login.microsoftonline.com'
tenant = '{TENANT}.onmicrosoft.com'
authority_uri = authority_host_uri + '/' + tenant
resource_uri = 'https://graph.microsoft.com/'
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"

context = adal.AuthenticationContext(authority_uri, api_version=None)
mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)
credentials = AADTokenCredentials(mgmt_token, client_id)
token = credentials.token['access_token']
uri = "https://graph.microsoft.com/beta/users/{USER}@{TENANT}.onmicrosoft.com/sendMail"
headers = {'Authorization': 'Bearer {}'.format(token)}
image = open('my.png', 'rb')
image_read = image.read()
result = base64.b64encode(image_read).decode('ascii')

mail = {
  "message": {
    "subject": "Graph Api Send Email Test",
    "body": {
      "contentType": "HTML",
      "content": "Graph Api Send Email Test"
    },
   'attachments' : [{
      '@odata.type' : "#microsoft.graph.fileAttachment",
      'contentBytes': result,
      'name' : "my.png"
    }],
    "toRecipients": [
      {
        "emailAddress": {
          "address": "recipient@email.com"
        }
      }
    ],
  }
}
r = requests.post(uri, headers=headers,json=mail)
print(r,r.content)

