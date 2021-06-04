import json
import uuid
import io
import binascii
import time

from PIL import Image, ImageDraw

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict

from django.contrib.auth            import get_user_model
from django.views.decorators.csrf   import csrf_exempt

from rest_framework.viewsets            import ModelViewSet
from rest_framework.views               import APIView
from rest_framework.decorators import api_view

from rest_framework.parsers             import MultiPartParser, FormParser, FileUploadParser
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

    def create(self, request, *args, **kwargs):

        print(request.data)
        # get serializer and do validating...
        serializer:object = self.get_serializer(data = request.data, many = False)
        serializer.is_valid(raise_exception = True)
        
        # create instance
        instance:object = serializer.save()

        # get success header, I don`t know what it is, but it was in documentation
        headers:dict = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = 201, headers = headers)

class ChatViewSet(ModelViewSetRedis):
    def get_queryset(self):
        queryset:QueryDict = self.request.user.get_chats()

        return queryset
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,]
    db_name = get_db_table_name(  Chat  )

    def _serialize_queryset(self, *args, **kwargs):
        queryset:QueryDict = self.get_queryset()
        print("i`m here")
        return self.serializer_class(queryset, user = self.request.user, *args, **kwargs).data



    


class TokenAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        print(request.data)
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
            print(error)
            return Response({"message":serializer.errors}, status = 400)

        # get user object
        user:User = serializer.validated_data['user']

        # get or create Token for current user
        token:Token
        created:bool
        token, created = Token.objects.get_or_create(user = user)

        return Response( { 'token':token.key, 'email': str(user.email) }, status = 201 if created else 200)



@api_view(['GET','POST','PATCH'])
def check(request):
    if request.method == 'PATCH':
        file_data = request.data['avatar']
        image = File(file_data)

    return Response({"message": "Hello, world!"})




