from rest_framework import serializers
from .models import Account
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Account.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ( 'password', 'password2', 'email')
        extra_kwargs = {
          #   'first_name': {'required': False},
          #   'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]+'_'+email.split('@')[1].split('.')[0]
        user = Account.objects.create(
            username=username,
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username','first_name','last_name','email',)