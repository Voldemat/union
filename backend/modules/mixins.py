from django.http import QueryDict

from rest_framework.viewsets            import ModelViewSet
from rest_framework.response            import Response

from cache.models       import redis_db as redis

class ModelViewSetRedis(ModelViewSet):
    def list(self, request):
        # get redis obj or None
        datalist = redis.get_list(prefix = self.db_name, json = True)

        # if redis obj does not exist
        if not datalist:
            queryset:QueryDict = self.get_queryset()
            datalist = self.get_serializer(queryset, many = True).data

            redis.set_list(
                prefix = self.db_name,
                datalist = datalist,
                ex = 60
            )
        return Response(datalist, status = 200)

    def retrieve(self, request, *args, **kwargs):
        # get instance_id
        instance_id:str = self.kwargs['pk']

        # get json object from redis
        obj_json:dict = redis.get(
            instance_id,
            json = True,
            prefix = self.db_name
        )
        # if json object does not exist
        if not obj_json:
            # get object from db
            obj:object          = self.get_object()

            # parse it into json
            serializer:object           = self.get_serializer(obj)
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

        return Response(obj_json, status = 200)