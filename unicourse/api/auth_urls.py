from django.urls import path
from .views import CurrentUserView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('me/', CurrentUserView.as_view(), name='auth_me'),
]