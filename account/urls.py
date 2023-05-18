from django.urls import path
from account.views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView

urlpatterns =[
    path('registr/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),       #метод as_view запускает именно тот метод который соответствует запросу(post, get, put ...)
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('change_pass/', ChangePasswordView.as_view()),
    path('forgot_pass/', ForgotPasswordView.as_view()),
    path('forg_pas_con/', ForgotPasswordCompleteView.as_view())
]