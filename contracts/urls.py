from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import viewtest
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registrations/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),   
    path('create/', views.start_contract, name='create_contract'),
    path('contract/<int:contract_id>/success/', views.contract_success, name='contract_success'),
    path('contract/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('oauth/', views.docusign_auth, name='docusign_auth'),
    path('callback/', views.docusign_callback, name='docusign_callback'),
    path('contract/sign/', views.sign_contract, name='sign_contract'),
]
