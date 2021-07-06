from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    BooleanField,
    DateTimeField,
    DurationField
)

from users.models import User, InviteToken


class FriendSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                FriendSerializer class
                It serialize friends field of user isntance

        """


        super(FriendSerializer, self).__init__(*args, **kwargs)

        return None
    class Meta:
        model = User
        exclude = (
            'last_login',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superuser',
            'user_permissions',
            'friends'
        )
        extra_kwargs = {
            '__all__':{'read_only': True}
        }


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                UserSerializer class.

                exclude fields = (
                    'last_login',
                    'is_active',
                    'is_staff',
                    'is_admin',
                    'is_superuser',
                    'user_permissions',
                    'friends'
                )
                Password field is write_only,
                and id   field is read_only.

                Also in this serializer overrided create method,
                due to hashing user password.
                
                This serializer is used at "/users" (look api_v1.views.UserViewSet)
        """


        super(UserSerializer, self).__init__(*args, **kwargs)

        return None

    friends = FriendSerializer(many = True)
    class Meta:
        model = User
        exclude = (
            'last_login',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superuser',
            'user_permissions'
        )
        extra_kwargs = {
            'password'  : {'write_only': True},
            'id'        : {'read_only': True}
        }

    def create(self, validated_data:dict) -> User:
        """
            [HELP DOCS]
                Overrided create method
                It use User.objects.create_user method
                to hash user password.

                It returns instance of User
        """
        instance:User = User.objects.create_user(**validated_data)
        return instance



class InviteTokenSerializer(ModelSerializer):
    user_invited = UserSerializer(many = False)
    user_inviting = UserSerializer(many = False)

    expired = BooleanField(required = False)
    time_to_expire = DurationField()
    class Meta:
        model = InviteToken
        exclude:tuple = (
            "updated_at",
            "expired_at"
        )