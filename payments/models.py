from django.db import models
from accounts.models import User
from transactions.models import Transaction

class Payment(models.Model):
    PAYMENT_TYPE = (
        ('utility', 'Utility Payment'),
        ('merchant', 'Merchant Payment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.amount}"

    @classmethod
    def make_payment(cls, user, payment_type, amount):
        """Handles payment creation and updates user transactions."""
        user_balance = cls.get_user_balance(user)

        if amount > user_balance:
            raise ValueError("Insufficient balance for this withdrawal.")

        payment = cls.objects.create(user=user, payment_type=payment_type, amount=amount)

        # Update transaction history
        Transaction.objects.create(user=user, transaction_type='transfer', amount=-amount)
        
        return payment

   