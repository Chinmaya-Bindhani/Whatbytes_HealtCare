from django.db import IntegrityError, transaction
from rest_framework import  serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as WeakPassword


class RegisterUserSerializer(serializers.Serializer):
    duplicate_email_message = "the email is already there ! "
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password= serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        email = User.objects.normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(self.duplicate_email_message)
        return email

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        email = validated_data["email"]

        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data)
        except IntegrityError:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    "email": [self.duplicate_email_message]
                })
            raise

    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('2 passwords arent matching with each other ')

        user = User(name=data["name"], email=data["email"])

        try:
            validate_password(data["password"], user=user)
        except WeakPassword as error:
            raise serializers.ValidationError({
                "password": error.messages
            })
        return data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return User.objects.normalize_email(value)


# user details
class ViewMe(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','email','name']
