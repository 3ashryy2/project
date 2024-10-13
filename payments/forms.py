from django import forms

class PaymentForm(forms.Form):
    payment_type = forms.ChoiceField(choices=[('utility', 'Utility Payment'), ('merchant', 'Merchant Payment')])
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
