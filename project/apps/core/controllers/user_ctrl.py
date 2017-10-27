from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from io import BytesIO
from PIL import Image
from core.models import User
from util import core_util
from util import error_msg
from util.constants import core_const

def create_thumbnail(user, image_url):
    THUMBNAIL_SIZE = (150, 150)
    if not image_url:
        return False

    FILE_TYPE = image_url.content_type

    if FILE_TYPE == 'image/png':
        PIL_FILE_TYPE = 'png'
    else:
        PIL_FILE_TYPE = 'jpeg'

    image = Image.open(image_url)
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_handle = BytesIO()
    image.save(temp_handle, PIL_FILE_TYPE)
    temp_handle.seek(0)

    thumbnail_name = "thumbnail_%s.%s" % ("_".join(str(s) for s in THUMBNAIL_SIZE), PIL_FILE_TYPE)
    suf = SimpleUploadedFile(thumbnail_name, temp_handle.read(), content_type=FILE_TYPE)
    user.thumbnail_image_url = suf
    return True

def update_image(user, files):
    if 'file' in files:
        image_file = files['file']
        user.image_url = image_file
        user.save()
        create_thumbnail(user, image_file)
        user.save()
        return user
    else:
        raise IntegrityError(error_msg.REQUIRED % "Image file")

def create_user(data):
    if User.objects.filter(user_name=data['user_name']).exists():
        raise IntegrityError(error_msg.ALREADY_EXISTS % data['user_name'])
    user = User.objects.create(**data)
    return user

def update_user(id, data):
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        raise IntegrityError(error_msg.NOT_EXISTS % 'User')

    mobile = None
    email = None

    if 'name' in data and data['name']:
        user.name = data['name'].strip().lower()
    if 'push_key' in data and data['push_key']:
        user.push_key = data['push_key']

    if 'password' in data and 'confirm_password' in data:
        if data['password'] and data['password'] == data['confirm_password']:
            user.password = data['password']
        else:
            raise IntegrityError('Password not matched')

    user.save()
    return user
