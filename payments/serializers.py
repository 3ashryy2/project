from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_type', 'amount']

    def validate_amount(self, value):
        # Ensure amount is greater than zero
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
