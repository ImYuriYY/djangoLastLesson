from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'fio', 'password']


    def save(self, **kwargs):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            fio = self.validated_data['fio']
        )
        password = self.validated_data['password']
        user.set_password(password)

        user.save()

        return user



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'