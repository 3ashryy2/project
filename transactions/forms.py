from django import forms

class DepositWithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
        

class SendMoneyForm(forms.Form):
    recipient = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
