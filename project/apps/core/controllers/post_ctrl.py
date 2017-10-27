from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from io import BytesIO
from core.models import Post
from util import error_msg
import av

def create_thumbnail(post, image_url):
    THUMBNAIL_SIZE = (300, 300)
    if not image_url:
        return False

    container = av.open(image_url)
    container = list(container.decode(video=0))
    frame = container[(int)(len(container) / 2)]

    PIL_FILE_TYPE = 'png'

    image = frame.to_image()
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_handle = BytesIO()
    image.save(temp_handle, PIL_FILE_TYPE)
    temp_handle.seek(0)

    thumbnail_name = "thumbnail_%s.%s" % ("_".join(str(s) for s in THUMBNAIL_SIZE), PIL_FILE_TYPE)
    suf = SimpleUploadedFile(thumbnail_name, temp_handle.read(), content_type=PIL_FILE_TYPE)
    post.thumbnail_image_url = suf
    return True


def create_post(data):
    post_data = {"title" : data['title'], "user" : data["user"]}

    if 'latitude' in data:
        post_data["latitude"] = data["latitude"]
    if 'longitude' in data:
        post_data["longitude"] = data["longitude"]
    if 'desc' in data:
        post_data["desc"] = data["desc"]
    if 'file' in data["file"]:
        post_data["url"] = data["file"]['file']

    post = Post.objects.create(**post_data)
    post.save()
    create_thumbnail(post , data["file"]['file'])
    post.save()
    return post
