from django.contrib.auth import login
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView


from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.permissions import IsAuthenticated 

from rest_framework.views import APIView
from django.contrib.auth import logout

class Logout(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)



class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UpdateUserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    
    queryset = CalculationHistory.objects.all()
    serializer_class = CalculationHistorySerializer


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        username = user.username
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data['username'] = username
        temp_list.data['user_id'] = user_id
        temp_list.data['first_name'] = first_name
        temp_list.data['last_name'] = last_name
        temp_list.data['email'] = email

        return Response({"data":temp_list.data})

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
