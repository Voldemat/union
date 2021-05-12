import redis
import json

from typing import Optional, Union


from django.conf import settings

from users.serializers import UserSerializer
from modules.utils import str_to_json


class Redis(redis.StrictRedis):
    def get(self, name:str, **kwargs:dict) -> Optional[str]:
        if 'prefix' in kwargs:
            # add prefix to name "prefix:name" ex. "users_user:1d259df6-3e38-4h2b-13gb-51d0c3ctee01"
            name = kwargs['prefix'] + ':' + str(name)

        try:
            # get value from redis and decode it
            value = super().get(name).decode('UTF-8')
        except AttributeError:
            # if value does not exist return None
            return None

        if 'json' in kwargs:
            # parse json from str
            value:dict = str_to_json(value)

        return value

    def set(self, name:str, value:Union[str, dict], **kwargs:dict) -> None:
        if 'json' in kwargs:
            # stringify json format
            value = str(value)

            # delete json kwarg
            del kwargs['json']

        if 'prefix' in kwargs:
            # add prefix to name "prefix:name" ex. "users_user:1d259df6-3e38-4h2b-13gb-51d0c3ctee01"
            name = kwargs['prefix'] + ':' + str(name)
            
            # delete prefix kwarg
            del kwargs['prefix']
            
        # call parent set method with additional kwargs
        super().set(name, value, **kwargs)

    def get_all(self, prefix:str, *args:list, **kwargs:dict) -> Optional[list]:
        all_obj:list[str] = list(self.scan_iter(f'{prefix}:*'))

        if 'json' in kwargs and kwargs['json'] == True:
            # serialize all str objects to json dictionary
            obj:str
            for obj in all_obj:
                # serialize object to json
                obj:dict = str_to_json(obj.decode('UTF-8'))

        return all_obj

    def set_list(self, prefix:str, datalist:list[dict], *args:list, **kwargs:dict) -> None:
        # serialize datalist into json
        value:str = json.dumps(datalist)

        name:str = prefix + '_list'

        self.set(
            name = name,
            value = value,
            **kwargs,
        )

        return None

    def get_list(self, prefix:str, *args:list, **kwargs:dict) -> Optional[   list[dict]  ]:
        name:str = prefix + '_list'

        redis_value = self.get(name = name)

        print(redis_value)
        datalist:list[dict] = str_to_json( redis_value )

        return datalist # list of json objects


redis_db = Redis(
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    db = 0
)

