from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, ProfileSerializer, TransactionSerializer
from transactions.models import Transaction

class RegisterView(APIView):
    """API endpoint for user registration."""
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = User.login_user(request, user.username, request.data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Create token for the user
                return Response({
                    'token': token.key,
                    'detail': "User registered successfully."
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """API endpoint for user login."""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user =User.login_user(request, username, password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)  # Get or create token
            return Response({
                'token': token.key,
                'detail': "Login successful."
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """API endpoint for user logout."""
    def post(self, request):
        User.logout_user(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

# Home API view
class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
        balance = sum(t.amount for t in Transaction.objects.filter(user=request.user))
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'balance': balance,
            'transactions': serializer.data
        }, status=status.HTTP_200_OK)




# Profile API view
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
