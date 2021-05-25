from django.http import QueryDict

from django.contrib.auth            import get_user_model

from rest_framework.viewsets            import ModelViewSet
from rest_framework.response            import Response
from rest_framework.permissions         import IsAuthenticated
from rest_framework.authtoken.views     import ObtainAuthToken
from rest_framework.authtoken.models    import Token


from users.serializers import UserSerializer

from modules.mixins import ModelViewSetRedis
from modules.utils import get_db_table_name

from chats.models import Chat, Message
from chats.serializers import ChatSerializer

class UserViewSet(ModelViewSetRedis):
    queryset:QueryDict = get_user_model().objects.all()
    serializer_class = UserSerializer

    db_name = get_db_table_name(  get_user_model()  )

class ChatViewSet(ModelViewSetRedis):
    def get_queryset(self):
        queryset:QueryDict = self.request.user.get_chats()

        return queryset
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,]
    db_name = get_db_table_name(  Chat  )

    


class TokenAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        help = "Handle POST request and get or create token from user credentials"
        # get serializer instance
        serializer:object = self.serializer_class(
            data = request.data,
            context = {"request":request}
        )

        # validating...
        serializer.is_valid(raise_exception = True)

        # get user object
        user:User = serializer.validated_data['user']

        # get or create Token for current user
        token:Token
        created:bool
        token, created = Token.objects.get_or_create(user = user)

        return Response( { 'token':token.key }, status = 201 if created else 200)