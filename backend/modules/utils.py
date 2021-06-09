import json
from typing import Optional, Union

from django.db.models import Model

from users.models import User

def get_db_table_name(model:Model) -> str:
    return model.objects.model._meta.db_table


def str_to_json(value:str) -> Optional[dict]:
    if not value:
        return None

    value = value.replace("\'",'\"')

    value = value.replace("None", "null")

    result = json.loads(value)

    return result






