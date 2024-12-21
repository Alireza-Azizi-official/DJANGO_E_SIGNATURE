from docusign_esign.client.api_exception import ApiException
from docusign_esign import ApiClient
import time
import jwt

DOCUSIGN_BASE_URL = "https://demo.docusign.net"
with open('contracts/private.key', 'r') as file:
    private_key = file.read()

current_time = int(time.time())
expiration_time = current_time + 3600  

payload = {
    "iss": '262cf28b-ab2e-4172-8c0e-91c2610b0322',
    "sub": '3809cbe5-630c-4736-a649-e60ba441aa2b',
    "aud": "account.docusign.com",
    "iat": current_time,
    "exp": expiration_time  
}

encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

def get_access_token():
    try:
        api_client = ApiClient()
        api_client.host = DOCUSIGN_BASE_URL
        api_client.set_oauth_host_name('account-d.docusign.com')

        token = api_client.request_jwt_application_token(
            client_id='262cf28b-ab2e-4172-8c0e-91c2610b0322',
            private_key_bytes=private_key.encode('utf-8'),
            expires_in=10800,  
            scopes=['signature'],
            oauth_host_name="account.docusign.com"
        )
        return token.access_token

    except ApiException as e:
        print(f"Error Code: {e.status}")
        print(f"Error Body: {e.body}")
        print(f"Error Reason: {e.reason}")
        print("Please verify your client ID, private key, or other JWT settings.")
        return None

token_jwt = get_access_token()

if token_jwt:
    print("Access Token (JWT):", token_jwt)
else:
    print("Failed to get access token using JWT.")
