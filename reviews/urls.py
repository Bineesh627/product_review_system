from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet,
    CustomAuthToken,
    LogoutViewSet,
)

router = DefaultRouter()

router.register(r'', UserRegistrationViewSet, basename='user')
router.register(r'', LogoutViewSet, basename='logout')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
]