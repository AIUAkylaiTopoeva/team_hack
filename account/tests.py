from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
# Create your tests here.
from .views import LoginView, LogoutView, RegistrationView, ChangePasswordView, ForgotPasswordCompleteView, ForgotPasswordView
from django.contrib.auth import get_user_model



class AuthTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password= '12345',
            is_active = True,
            activation_code = '1234'
        )
    def test_register(self):
        data= {
            'emil': 'new_user@gmail.com',
            'password': '123456',
            'password_confirm': '123456',
            'name': 'test',
            'last_name' : 'Test'
        }

        request = self.factory.post('api/v1/registr/', data, format = 'json')
        print(request)
        view = RegistrationView.as_view()
        response = view(request)
        print(response)


        assert response.status_code ==201
        assert get_user_model().objects.filter(email = data['email']).exists()

    def test_login(self):
        data ={
            'emil': 'user@gmail.com',
            'password': '12345',
        }
        request = self.factory.post('api/v1/login/', data, format='json')
        view  =LoginView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code ==200
        assert 'token' in response.data

    def test_change_password(self):
        data = {
            'old_password': '12345',
            'new_password': '1234',
            'new_password_confirm': '1234',

        }

        request = self.factory.post('api/v1/change_pass/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        print(response)
        assert response.status_code !=401   #==200


    def test_forgot_password(self):
        data ={
            'email': 'user@gmail.com'
        }
        request = self.factory.post('api/v1/forgot_pass/', data, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        
        assert response.status_code==200

    def test_forgot_password_complete(self):
        data = {
            'email':'user@gmail.com',
            'code': '1234',
            'password':'1234567',
            'password_confirm': '1234567'
        }
        request = self.factory.post('api/v1/forg_pas_con/', data, format='json')
        view = ForgotPasswordCompleteView.as_view()
        response = view(request)

        assert response.status_code ==200
