from django.urls import path
from .views import MakePaymentAPIView

urlpatterns = [
    path('make-payment/', MakePaymentAPIView.as_view(), name='api_make_payment'),
]