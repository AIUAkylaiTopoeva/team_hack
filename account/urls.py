from django.urls import path
from account.views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView
from django.views.decorators.cache import cache_page

urlpatterns =[
    path('registr/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),       #метод as_view запускает именно тот метод который соответствует запросу(post, get, put ...)
    path('login/',cache_page(60*5)(LoginView.as_view())),
    path('logout/',LogoutView.as_view()),
    path('change_pass/', cache_page(60*5)(ChangePasswordView.as_view())),
    path('forgot_pass/', ForgotPasswordView.as_view()),
    path('forg_pas_con/', ForgotPasswordCompleteView.as_view())
]