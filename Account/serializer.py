from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','phone','password')
        extra_kwargs = {'password': {'write_only' : True},}

        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone',)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style = { 'input_type': 'password'}, trim_whitespace = False
    )

    def validate(self, data):
        print(data)
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            if User.objects.filter(username = phone).exists():
                print(phone, password)
                user = authenticate(request = self.context.get('request'), username = phone, password = password)
                print(user)

            else:
                msg = {
                    'detail' : 'Username number not found',
                    'status' : False,
                }
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail' : 'Username and password not matching. Try again',
                    'status' : False,
                }
                raise serializers.ValidationError(msg, code = 'authorization')


        else:
            msg = {
                    'detail' : 'Phone number and password not found in request',
                    'status' : False,
                }
            raise serializers.ValidationError(msg, code = 'authorization')

        data['user'] = user
        return data