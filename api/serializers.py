from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.location import Location
from .models.mango import Mango
from .models.bin import Bin
from api.models.order_bin import Order_Bin
from .models.route import Route

class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

class LocationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Location
        fields = ('id', 'street', 'city', 'state', 'zip_code', 'property_type', 'user', 'route', 'email')

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ('id', 'barcode', 'active','location_id','location', 'bin_model_foreign_key', 'model')

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id','day_of_week', 'user_id')

class Order_BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Bin
        fields = ('id', 'order_date', 'fulfilled_date', 'status', 'location_id', 'bin_model_id')

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
