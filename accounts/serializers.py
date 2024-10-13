from rest_framework import serializers
from transactions.models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    pin = serializers.CharField(write_only=True, min_length=4, max_length=4)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'pin')

    def create(self, validated_data):
        return User.register_user(validated_data)



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'created_at']
