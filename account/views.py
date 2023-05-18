from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .permissions import IsActivePermission
from .serializers import RegistrationSerialazer, ActivationSerialazer,LoginSerialazer,  ChangePasswordSerialazer, ForgotPasswordSerialazer, ForgotPasswordCompleteSerializer

#APIView - класс

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerialazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=200)
    
class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerialazer(data=request.data)      
        serializer.is_valid(raise_exception= True)         #проверяет на все проверки
        serializer.activate()
        return Response('Аккаунт успешно активирован', status=200)
    
class LoginView(ObtainAuthToken):         #Token - ключ,вход                         
    serializer_class = LoginSerialazer

class LogoutView(APIView):
    permission_classes = [IsActivePermission]
    def post(self,request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('You logout from your account')
    
class ChangePasswordView(APIView):
    permission_classes = (IsActivePermission,)
    def post(self, request):
        serializer = ChangePasswordSerialazer(data = request.data, context={'request':request})    #context- словарь с какими-то данными, все что связано с запросами . С context можно вытаскивать ...
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Status: 200. Password sucsessfuly changed')

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerialazer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Мы выслали сообщение для востановления')
        
class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('password sucsessfully changed')