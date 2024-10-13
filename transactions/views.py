from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import DepositWithdrawSerializer, SendMoneySerializer
from .models import Transaction

class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']

            if not request.user.check_pin(pin):
                return Response({"error": "Invalid PIN."}, status=status.HTTP_400_BAD_REQUEST)
            # Call the deposit model method
            Transaction.deposit(user=request.user, amount=amount)
            return Response({"detail": "Deposit successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']

            if not request.user.check_pin(pin):
                return Response({"error": "Invalid PIN."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Call the withdraw model method
                Transaction.withdraw(user=request.user, amount=amount)
                return Response({"detail": "Withdrawal successful."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMoneyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendMoneySerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            recipient = serializer.validated_data['recipient']
            pin = serializer.validated_data['pin']

            if not request.user.check_pin(pin):
                return Response({"error": "Invalid PIN."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Call the send_money model method
                Transaction.send_money(sender=request.user, recipient_username=recipient, amount=amount)
                return Response({"detail": "Money sent successfully."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
