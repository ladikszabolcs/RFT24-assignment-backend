from django.urls import path
from .views import CurrentUserView
from .views import CustomAuthToken

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('me/', CurrentUserView.as_view(), name='auth_me'),
]