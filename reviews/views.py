from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .permissions import IsAdminUser, IsRegularUser
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .serializers import UserRegistrationSerializer, ProductSerializer, ReviewSerializer
from .models import Product, Review
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsRegularUser]
    
    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        try:
            product = get_object_or_404(Product, pk=product_id)
            return Review.objects.filter(product_id=product_id)
        except Exception as e:
            raise ValidationError({"detail": str(e)})
    
    def perform_create(self, serializer):
        product_id = self.kwargs['product_pk']
        try:
            product = get_object_or_404(Product, pk=product_id)
            
            # Check for existing review
            if Review.objects.filter(product=product, user=self.request.user).exists():
                raise ValidationError(
                    {"detail": "You have already reviewed this product."},
                    code=status.HTTP_400_BAD_REQUEST
                )
                
            serializer.save(user=self.request.user, product=product)
        except IntegrityError as e:
            raise ValidationError(
                {"detail": "Database error occurred while creating review."},
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            raise ValidationError(
                {"detail": str(e)},
                code=status.HTTP_400_BAD_REQUEST
            )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserRegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {"message": "User created successfully"}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, 
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except Exception as e:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            return Response(
                {"detail": "Logout failed"},
                status=status.HTTP_400_BAD_REQUEST
            )