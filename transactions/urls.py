from django.urls import path
from .views import DepositAPIView, WithdrawAPIView, SendMoneyAPIView

urlpatterns = [
    path('deposit/', DepositAPIView.as_view(), name='api_deposit'),
    path('withdraw/', WithdrawAPIView.as_view(), name='api_withdraw'),
    path('send-money/', SendMoneyAPIView.as_view(), name='api_send_money'),
]
