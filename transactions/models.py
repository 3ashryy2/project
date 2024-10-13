from django.db import models
from accounts.models import User

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"

    @staticmethod
    def get_user_balance(user):
        """Returns the user's balance by summing up their transactions."""
        return sum(t.amount for t in Transaction.objects.filter(user=user))

    @classmethod
    def deposit(cls, user, amount):
        """Create a deposit transaction."""
        return cls.objects.create(user=user, transaction_type='deposit', amount=amount)

    @classmethod
    def withdraw(cls, user, amount):
        """Create a withdrawal transaction."""
        balance = cls.get_user_balance(user)
        if amount > balance:
            raise ValueError("Insufficient balance for this withdrawal.")
        return cls.objects.create(user=user, transaction_type='withdraw', amount=-amount)

    @classmethod
    def send_money(cls, sender, recipient_username, amount):
        """Transfer money from the sender to the recipient."""
        balance = cls.get_user_balance(sender)
        if amount > balance:
            raise ValueError("Insufficient balance to send money.")
        
        recipient = User.objects.filter(username=recipient_username).first()
        if not recipient:
            raise ValueError(f"User '{recipient_username}' does not exist.")

        # Debit the sender's account
        cls.objects.create(user=sender, transaction_type='transfer', amount=-amount)
        # Credit the recipient's account
        cls.objects.create(user=recipient, transaction_type='transfer', amount=amount)
        return True
