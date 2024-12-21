from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient
from docusign_esign.client.api_exception import ApiException
from docusign_esign.models import RecipientViewRequest
from .docusign_auth import get_access_token

from .forms import RegisterForm, ContractForm
from .models import Contract
from core import settings
import urllib.parse
import requests
import base64

access_token = settings.DOCUSIGN_ACCESS_TOKEN
account_id = settings.DOCUSIGN_ACCOUNT_ID
base_url = "https://demo.docusign.net/restapi"  
auth_header = {"Authorization": f"Bearer {access_token}"}
DOCUSIGN_BASE_URL = 'https://demo.docusign.net'
DOCUSIGN_REDIRECT_URI = settings.DOCUSIGN_REDIRECT_URI

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'contracts/register.html', {'form':form})
    
@login_required
def home(request):
    return render(request, 'contracts/home.html')

def create_api_client():
    access_token = get_access_token()  
    if not access_token:
        raise Exception("access token not available")

    api_client = ApiClient()
    api_client.host = DOCUSIGN_BASE_URL
    api_client.set_default_header('authorization', f'Bearer {access_token}')
    return api_client

def start_contract(request):
    contract_text= '''
    It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. 
    The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using Content here, content here, 
    making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, 
    and a search for lorem ipsum will uncover many web sites still in their infancy. Various versions have evolved over the years, 
    sometimes by accident, sometimes on purpose. Please sign the contract here: ~signature~
    '''
    contract_base64 = base64.b64encode(contract_text.encode('utf-8')).decode('utf-8')
    
    contract = None
    if request.method == 'POST':
        signer_email = request.POST.get('email')
        signer_name = request.POST.get('name')
        contract_text = contract_base64  
        access_token = get_access_token()
        
        if not access_token:
            return render(request, 'contracts/create_contract.html', {
                'error': 'failed to authenticate with docusign',
                'contract_text': base64.b64decode(contract_base64).decode('utf-8') 
            })
        try:
            api_client = create_api_client(DOCUSIGN_BASE_URL, access_token) 
            document = Document(
                document_base64=contract_text.encode('utf-8').decode('utf-8'), 
                name='Contract',
                file_extension='txt',
                document_id='1'
            )

            signer = Signer(
                email=signer_email,
                name=signer_name,
                recipient_id='1',
                routing_order='1',
                tabs={ 'sign_here_tabs': [ 
                    { 'x_position': 100, 'y_position': 100, 'document_id': '1', 'page_number': '1' } 
                ]}
            )

            envelope_definition = EnvelopeDefinition(
                email_subject="please sign the contract",
                documents=[document],
                recipients={"signers": [signer]},
                status="sent"
            )

            envelope_api = EnvelopesApi(api_client)
            envelope_summary = envelope_api.create_envelope(account_id, envelope_definition)
            envelope_id = envelope_summary.envelope_id

            if not envelope_id:
                return render(request, 'contracts/create_contract.html', {'error': 'failed to create envelope with docusgin'})

            send_signing_email(signer_email, envelope_id)

            contract = Contract.objects.create(
                user=request.user,
                envelope_id=envelope_id,
                recipient_email=signer_email,
                recipient_name=signer_name,
                status='sent'
            )
            contract.save()

            status = check_envelope_status(envelope_id)
            if status == 'completed':
                contract.status = 'completed'
                contract.save()
                return redirect('contracts/contract_success.html', contract_id=contract.id)
            else:
                return render(request, 'contracts/create_contract.html', {'status': status, 'contract': contract})
            
        except Exception as e:
            return render(request, 'contracts/create_contract.html', {
                'error': 'an error occurred',
                'contract_text': base64.b64decode(contract_base64).decode('utf-8')
            })
    else:
        return render(request, 'contracts/create_contract.html')


def check_envelope_status(envelope_id):
    access_token = get_access_token()
    if not access_token:
        return None
    
    api_client = ApiClient()
    api_client.host = base_url
    api_client.set_default_header('authorization', f'Bearer {access_token}')
    envelope_api = EnvelopesApi(api_client)
    envelope_status = envelope_api.get_envelope(account_id=account_id, envelope_id=envelope_id)
    return envelope_status.status
 
def create_recipient_view(access_token, envelope_id, recipient_email):
    api_client = create_api_client()  
    recipient_view_request = RecipientViewRequest(
        return_url=DOCUSIGN_REDIRECT_URI,  
        recipient_id='1',
        authentication_method='email',
        email=recipient_email
    )

    try:
        envelope_api = EnvelopesApi(api_client)
        recipient_view = envelope_api.create_recipient_view(account_id, envelope_id, recipient_view_request)
        return recipient_view.url 
    except ApiException as e:
        print(f"Error: {e}")
        return None



def send_signing_email(recipient_email, envelope_id):
    access_token = get_access_token()  
    signing_url = create_recipient_view(access_token, envelope_id, recipient_email)
    
    if signing_url:
        subject = 'invitation to sign the contract'
        message = f'please sign the contract using the following link: {signing_url}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [recipient_email]
        send_mail(subject, message, from_email, recipient_list)
        return signing_url
    else:
        print("error generating signing URL.")
        
def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    updated_status = get_contract_status(contract)
    return render(request, 'contracts/contract_detail.html', {'contract': contract, 'status': updated_status})

def get_contract_status(envelope_id):
    try:
        api_client = create_api_client()  
        envelope_api = EnvelopesApi(api_client)
        envelope_status = envelope_api.get_envelope(account_id, envelope_id)
        return envelope_status.status
    except ApiException as e:
        print(f"Error: {e}")
        return None

def contract_success(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    return render(request, 'contracts/contract_success.html', {'contract': contract})

def docusign_auth(request):
    auth_url = settings.DOCUSIGN_AUTH_URL
    redirect_uri = settings.DOCUSIGN_REDIRECT_URI
    client_id = settings.DOCUSIGN_CLIENT_ID
    params = {
        'response_type': 'code', 
        'scope': 'signature', 
        'client_id': client_id,  
        'redirect_uri': redirect_uri  
    }
    url = f'{auth_url}?{urllib.parse.urlencode(params)}'
    return redirect(url)

def docusign_callback(request):
    code = request.GET.get('code')
    token_url = settings.DOCUSIGN_TOKEN_URL
    data = {
        'grant_type': 'authorization_code', 
        'code': code,  
        'redirect_uri': settings.DOCUSIGN_REDIRECT_URI, 
        'client_id': settings.DOCUSIGN_CLIENT_ID, 
        'client_secret': settings.DOCUSIGN_CLIENT_SECRET  
    }
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        request.session['docusign_access_token'] = access_token
        return redirect(request, 'contracts/success.html') 
    else:
        return redirect(request, 'contracts/error.html')

def sign_contract(request):
    contract_id = request.GET.get('contract_id')
    contract = get_object_or_404(Contract, id=contract_id)

    if request.method == 'POST':
        contract.signed_by_recipient = True  
        contract.signed_at_recipient = contract.end_date  
        contract.status = 'signed'  
        contract.save()
        messages.success(request, f'Contract {contract.envelope_id} has been signed by the recipient!')
        return redirect('contract_detail', pk=contract.pk)

    return render(request, 'contracts/sign_contract.html', {'contract': contract})