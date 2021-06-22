from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
)

from users.models import User, Friend


class FriendModelUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "about_me",
            "avatar"
        )
    read_only_fields = "__all__" 

class FriendSerializer(ModelSerializer):
    friend = FriendModelUserSerializer(many = False)
    class Meta:
        model = Friend
        fields = (
            "friend",
        )


class UserSerializer(ModelSerializer):
    friends = FriendSerializer(source = 'get_friends', many = True)
    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_staff', 'is_admin']
        extra_kwargs = {
            'password'  : {'write_only': True},
            'id'        : {'read_only': True}
        }

    def create(self, validated_data) -> User:
        obj = User.objects.create_user(**validated_data)
        return obj

