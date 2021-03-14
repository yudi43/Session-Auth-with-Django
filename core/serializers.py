from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


# The reason that we are using two serializers for the models is that we'll be using the UserSerializerWithToken
# for handling signups. When a user signs up, we want the response from the server to include both their relevant 
# user data (in this case, just the username), as well as the token.

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username')

class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only = True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')
        