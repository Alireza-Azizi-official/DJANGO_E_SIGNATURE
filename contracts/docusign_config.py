import environ

env = environ.Env()
environ.Env.read_env()

DOCUSIGN_BASE_URL="https://demo.docusign.net"
DOCUSIGN_CLIENT_ID="262cf28b-ab2e-4172-8c0e-91c2610b0322"
DOCUSIGN_CLIENT_SECRET="51748354-84c5-419f-88ec-0d5957af2500"
DOCUSIGN_USER_ID="d93f9c9a-d2b9-4297-aee3-b26dbeb25bda"
DOCUSIGN_REDIRECT_URI="https://e056-89-41-12-29.ngrok-free.app/docusign/callback/"
with open('contract/private.key', 'r') as file:
    DOCUSIGN_PRIVATE_KEY = file.read()
    

