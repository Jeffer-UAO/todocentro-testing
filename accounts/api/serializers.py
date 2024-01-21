from rest_framework import serializers
from accounts.models import Account, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'phone_number', 'username', 'email', 'first_name',
                  'last_name', 'password', 'is_active', 'is_staff']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'title', 'name_lastname', 'address',
                  'city', 'country', 'active', 'phone', 'user']