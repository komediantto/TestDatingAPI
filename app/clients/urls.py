from django.urls import path
from .views import client_create, client_list, match
from rest_framework.authtoken import views


urlpatterns = [
    path('clients/api-token-auth/', views.obtain_auth_token),
    path('clients/create/', client_create, name='client-create'),
    path('clients/list/', client_list, name='client-list'),
    path('clients/<int:pk>/match/', match, name='match')
]
