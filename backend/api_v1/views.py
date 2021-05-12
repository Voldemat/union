from django.http import QueryDict

from django.contrib.auth            import get_user_model

from rest_framework.viewsets            import ModelViewSet
from rest_framework.response            import Response
from rest_framework.authtoken.views     import ObtainAuthToken
from rest_framework.authtoken.models    import Token

from cache.models       import redis_db as redis
from users.serializers import UserSerializer

from modules.utils import get_db_table_name

class UserViewSet(ModelViewSet):
    queryset:QueryDict = get_user_model().objects.all()
    serializer_class = UserSerializer

    db_name = get_db_table_name(  get_user_model()  )
    
    def list(self, request):
        # get redis obj or None
        datalist = redis.get_list(prefix = self.db_name, json = True)
        status = 200

        # if redis obj does not exist
        if not datalist:
            queryset:QueryDict = self.get_queryset()
            datalist = self.get_serializer(queryset, many = True).data

            redis.set_list(
                prefix = self.db_name,
                datalist = datalist,
                ex = 60
            )

            status = 201
        return Response(datalist, status = status)

    def retrieve(self, request, *args, **kwargs):
        # get user_id
        user_id:str = self.kwargs['pk']

        # get json object from redis
        obj_json:dict = redis.get(
            user_id,
            json = True,
            prefix = self.db_name
        )

        # if json object does not exist
        if not obj_json:

            # get object from db
            obj:User          = self.get_object()

            # parse it into json
            serializer:UserSerializer   = self.get_serializer(obj)
            obj_json:dict               = serializer.data

            # set json object into redis db
            redis.set(
                name = obj_json['id'],
                value = obj_json,
                json = True,
                prefix = self.db_name,
                # ex = expiry
                ex = 60
            )

        return Response(obj_json)


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