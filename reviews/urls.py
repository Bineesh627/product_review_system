from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet,
    CustomAuthToken,
    LogoutViewSet,
    ProductViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register('', UserRegistrationViewSet, basename='user')
router.register('', LogoutViewSet, basename='logout')
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('products/<int:product_pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
]