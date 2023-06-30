import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Client


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class ClientSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)
    longitude = serializers.DecimalField(required=True, max_digits=9,
                                         decimal_places=6)
    latitude = serializers.DecimalField(required=True, max_digits=9,
                                        decimal_places=6)

    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name',
                  'password', 'avatar', 'sex', 'email',
                  'latitude', 'longitude']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Client(**validated_data)
        user.set_password(password)
        user.save()
        return user
