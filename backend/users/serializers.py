from rest_framework.serializers import ModelSerializer, StringRelatedField

from users.models import User


class FriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "about_me",
            "avatar"
        )


class UserSerializer(ModelSerializer):
    friends = FriendSerializer(many = True)
    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_staff', 'is_admin']
        extra_kwargs = {
            'password'  : {'write_only': True},
            'id'        : {'read_only': True},
            "friends"   : {'required':False}
        }

    def create(self, validated_data):
        obj = get_user_model().objects.create_user(**validated_data)
        return obj

