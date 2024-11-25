from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, LectureViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'lectures', LectureViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('api.auth_urls')),  # Token authentication URLs
]