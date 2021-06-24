from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
)

from users.models import User, Friend


class FriendModelUserSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                Friend User Read Only Serializer.
                It serialize only friend field of Friend istance.
                It is used in FriendsSerializer defined below to serialize
                user(friend).

                fields = (
                    "id",
                    "email",
                    "first_name",
                    "last_name",
                    "birth_date",
                    "about_me",
                    "avatar"
                )

        """

        super(FriendModelUserSerializer, self).__init__(*args, **kwargs)

        return None


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
    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                FriendSerializer class
                It serialize Friend instance,
                but only friend field, uses FriendModelUserSerializer defined
                above.
                This serializer is used at "/friends" endpoint to serialize user friends.

                For additional info see api_v1.views.FriendsAPIView

        """


        super(FriendSerializer, self).__init__(*args, **kwargs)

        return None
    friend = FriendModelUserSerializer(many = False)
    class Meta:
        model = Friend
        fields = (
            "friend",
        )


class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                UserSerializer class.

                exclude fields = (
                    'last_login',
                    'is_active',
                    'is_staff',
                    'is_admin'
                )
                Password field is write_only,
                and id   field is read_only.

                Also in this serializer overrided create method,
                due to hashing user password.
                
                This serializer is used at "/users" (look api_v1.views.UserViewSet)
        """


        super(UserSerializer, self).__init__(*args, **kwargs)

        return None

    friends = FriendSerializer(source = 'get_friends', many = True)
    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_staff', 'is_admin']
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

    # def is_valid(self, *args, **kwargs) -> None:
    #     print('is_valid')
    #     try:
    #         super(UserSerializer, self).is_valid(*args, **kwargs)
    #     except serializers.ValidationError as error:
    #         print(error)
    #     raise Exception()

    #     return None

