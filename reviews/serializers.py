from rest_framework import serializers
from .models import Product, Review, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        try:
            validated_data.pop('password2')
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"username": "A user with that username already exists."}
            )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'average_rating']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'description': {'required': False},
            'price': {
                'required': True,
                'min_value': 0.01,
                'max_digits': 10,
                'decimal_places': 2
            }
        }

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'feedback', 'created_at']
        read_only_fields = ['user', 'created_at']
        extra_kwargs = {
            'rating': {
                'required': True,
                'min_value': 1,
                'max_value': 5
            },
            'feedback': {
                'required': True,
                'allow_blank': False,
                'max_length': 1000
            }
        }
    
    def validate(self, data):
        product = self.context.get('product')
        user = self.context.get('request').user
        
        if self.instance is None and Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError(
                {"detail": "You have already reviewed this product."}
            )
        return data