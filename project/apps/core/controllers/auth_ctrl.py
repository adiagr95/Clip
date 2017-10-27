from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from conf import SESSION_ACTIVE
from core.models import User, Secret
from util import core_util
from util import error_msg
from util.constants import core_const


def create_session(user_id, data):
    if User.objects.filter(id=user_id):
        user = User.objects.get(id=user_id)
    else:
        raise IntegrityError(error_msg.NOT_EXISTS % "User")

    secret_data = {
        'user': user
    }
    if 'push_key' in data and data['push_key']:
        secret_data['push_key'] = data['push_key']
        user.push_key = data['push_key']
        user.save()
    if 'device_id' in data and data['device_id']:
        secret_data['device_id'] = data['device_id']
    if 'client_type' in data and data['client_type']:
        secret_data['client_type'] = data['client_type']
    secret = Secret.objects.create(**secret_data)
    return {'user': user.get_data(), 'secret': secret.id}


def check_auth(data):
    current_time = core_util.get_current_time()
    if not SESSION_ACTIVE:
        return {}
    if 'user_id' in data and data['user_id'] and 'secret' in data and data['secret']:
        try:
            user = User.objects.get(id=data['user_id'])
        except ObjectDoesNotExist:
            raise IntegrityError(error_msg.NO_AUTH)

        if user.secrets.filter(id=data['secret'], expiry__gt=current_time):
            secret = user.secrets.get(id=data['secret'], expiry__gt=current_time)
            secret.expiry = core_util.add_time(core_const.SECRET_TTL)
            secret.save()
            return user
        else:
            raise IntegrityError(error_msg.NO_AUTH)
    else:
        raise IntegrityError(error_msg.NO_AUTH)
