from django.http          import QueryDict
from django.contrib.auth  import get_user_model

from rest_framework.views               import APIView    
from rest_framework.serializers         import ModelSerializer
from rest_framework.response            import Response
from rest_framework.permissions         import IsAuthenticated
from rest_framework.authtoken.views     import ObtainAuthToken
from rest_framework.authtoken.models    import Token

from users.models import User
from users.serializers import UserSerializer, FriendSerializer

from modules.mixins import ModelViewSetRedis
from modules.utils import get_db_table_name

from chats.models import Chat, Message
from chats.serializers import ChatSerializer

class UserViewSet(ModelViewSetRedis):
    queryset:QueryDict = get_user_model().objects.all()
    serializer_class:ModelSerializer = UserSerializer

    db_name:str = get_db_table_name(  get_user_model()  )

class ChatViewSet(ModelViewSetRedis):
    serializer_class:ModelSerializer = ChatSerializer

    permission_classes:list = [IsAuthenticated,]

    db_name:str = get_db_table_name(  Chat  )

    def get_queryset(self):
        queryset:QueryDict = self.request.user.get_chats()
        return queryset


    def _serialize_queryset(self, *args, **kwargs):
        queryset:QueryDict = self.get_queryset()
        return self.serializer_class(queryset, user = self.request.user, *args, **kwargs).data




class TokenAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        help = "Handle POST request and get or create token from user credentials"
        # get serializer instance
        serializer:object = self.serializer_class(
            data = request.data,
            context = {"request":request}
        )

        # validating...
        try:
            serializer.is_valid(raise_exception = True)
        except Exception as error:
            return Response({"message":serializer.errors}, status = 400)

        # get user object
        user:User = serializer.validated_data['user']

        # get or create Token for current user
        token:Token
        created:bool
        token, created = Token.objects.get_or_create(user = user)

        return Response( { 'token':token.key, 'email': str(user.email) }, status = 201 if created else 200)



class FriendsAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, format = None):
        user:User = request.user

        try:
            queryset:QueryDict          = request.user.get_friends()
            print(queryset)
            serializer:FriendSerializer = FriendSerializer(queryset, many = True)

        except Exception:
            return Response({"error":serializer.errors}, status = 400)
        return Response(serializer.data, status = 200)

