from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail

User = get_user_model()


class RegistrationSerialazer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(min_length=4, required = True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким имейлом уже существует')
        return email
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('passwords is not same')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        print(user) 
        return user
    
class ActivationSerialazer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email= email, activation_code = code).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return attrs
    
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active=True
        user.activation_code = ''
        user.save()
        return 
    
class LoginSerialazer(serializers.Serializer):
    
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email нет')
        return email
    
    def validate(self, data):
        request = self.context.get('request')      #context-функция Python, которая принимает объект запроса в качестве аргумента и возвращает словарь, добавляемый в контекст запроса.  context- словарь с какими-то данными, все что связано с запросами . С context можно вытаскивать
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user= authenticate(username = email,
                               password = password,
                               request=request)
            if not user:
                raise serializers.ValidationError('Не верный email или пароль')
        else:
            raise serializers.ValidationError('Email и пароль обязательны к заполнению')
        data['user']=user      #изначально в data словаре нет значения user, мы его добавили
        return data
    
class ChangePasswordSerialazer(serializers.Serializer):     #мы наследуемся от потому что мы сами можем задавать поля
    old_password = serializers.CharField(min_length = 4, required=True)
    new_password = serializers.CharField(min_length = 4, required=True)
    new_password_confirm = serializers.CharField(min_length = 4, required=True)

    def validate_old_password(self, old_password):
        request= self.context.get('request')
        user = request.user
        if not user.check_password(old_password):     #проверяет пароль и под капотом хэширует его
            raise serializers.ValidationError('Вы ввели некорректный пароль')
        return old_password
    
    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')
        new_pass_con = data.get('new_password_confirm')
        if new_pass !=new_pass_con:
            raise serializers.ValidationError('Пароли не совпадают')
        if old_pass ==new_pass:
            raise serializers.ValidationError('Пароль должен отличаться от прошлых')
        return data
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()



# email, на него будет отправлен код подтвержденияб потом мы его будем проверять
# send_mail
# send_veritication_email, 
# пароль меняем на новый пароль. Те же самые проверки

class ForgotPasswordSerialazer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email нет')
        return email
    

    def send_verification_email(self):
        email=self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail('Восстановление пароля',f'Ваш код восстановления {user.activation_code}','test@gmail.com',[user.email])

    
    

class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.CharField()
    code= serializers.CharField()
    password = serializers.CharField(min_length = 4, required=True)
    password_confirm = serializers.CharField(min_length = 4, required=True)
    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        passw = data.get('password')
        pass_con = data.get('password_confirm')
        if not User.objects.filter(email=email, activation_code = code).exists():
            raise serializers.ValidationError('Пользователь с таким email нет')
        if passw !=pass_con:
            raise serializers.ValidationError('Пароли не совпадают')
        return data
        
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email = email)
        user.set_password(password)
        user.activation_code = ''
        user.save()