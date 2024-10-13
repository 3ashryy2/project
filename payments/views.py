from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer

class MakePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access this endpoint

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            payment_type = serializer.validated_data['payment_type']
            user = request.user

            try:
                # Call model method to handle payment logic
                Payment.make_payment(user=user, payment_type=payment_type, amount=amount)
                return Response({"detail": "Payment successful."}, status=status.HTTP_200_OK)
            
            except ValueError as e:
                # Handle insufficient balance or other business logic errors
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return validation errors from serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
