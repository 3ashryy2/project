from rest_framework import serializers
from .models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'created_at']

class DepositWithdrawSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True)
    class Meta:
        model = Transaction
        fields = ['amount','pin']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    def validate_pin(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("PIN must be 4 digits.")
        return value

class SendMoneySerializer(serializers.Serializer):
    recipient = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    pin = serializers.CharField(write_only=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    def validate_recipient(self, value):
        try:
            recipient = User.objects.get(username=value)
            return recipient
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient does not exist.")
        
    def validate_pin(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("PIN must be 4 digits.")
        return value