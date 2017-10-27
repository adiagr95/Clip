import os

from django.db import models
from django.db.models import Q
import json
from util import core_util
from util.constants import core_const

def update_user_image(instance, filename):
    return os.path.join('logos', instance.name + '_' + filename)


def update_user_thumbnail_image(instance, filename):
    return os.path.join('logo_thumbnails', instance.name + '_' + filename)

def update_post_video(instance, filename):
    return os.path.join('posts', instance.title + '_' + filename)

def update_post_thumbnail_image(instance, filename):
    return os.path.join('posts_thumbnails', instance.title + '_' + filename)

class User(models.Model):
    id = models.AutoField(primary_key=True)

    user_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(max_length=200, default='', blank=True, null=True)
    image_url = models.FileField(upload_to=update_user_image, null=True, blank=True)
    thumbnail_image_url = models.FileField(upload_to=update_user_thumbnail_image, null=True, blank=True)
    password = models.CharField(max_length=100, default='', blank=False, null=False)
    push_key = models.TextField(max_length=2000, default='', null=True, blank=True)
    device_id = models.TextField(max_length=1000, default='', null=True, blank=True)

    is_account_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ('name',)

    def __str__(self):
        if self.name:
            return self.name
        return self.user_name

    def get_data(self):
        data = {"id" : self.id ,
            "user_name" : self.user_name,
            "push_key" : self.push_key,
            "device_id" : self.device_id,
            "is_account_active" : self.is_account_active
        }
        if self.name:
            data["name"] = self.name
        else:
            data["name"] = self.user_name
        if self.thumbnail_image_url:
            data['thumbnail_image_url'] = "https://s3.amazonaws.com/uifaces/faces/twitter/ladylexy/128.jpg"
        if self.image_url:
            data['image_url'] = self.image_url.url
        return data

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = core_util.get_current_time()
        self.updated_at = core_util.get_current_time()

        return super(User, self).save(*args, **kwargs)

class Post(models.Model):
    id = models.AutoField(primary_key=True)

    url = models.FileField(upload_to=update_post_video, null=True, blank=True)
    thumbnail_image_url = models.FileField(upload_to=update_post_thumbnail_image, null=True, blank=True)
    title = models.TextField(max_length=500, default='', blank=True, null=True)
    desc = models.TextField(max_length=1000, default='', blank=True, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    user = models.ForeignKey('core.User', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def get_data(self):
        data = {"id" : self.id ,
            "title" : self.title,
            "desc" : self.desc,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "created_at" : self.created_at
        }
        if self.url:
            data["url"] = self.url.url
        if self.thumbnail_image_url:
            # data["thumbnail_image_url"] = self.thumbnail_image_url.url
            data["thumbnail_image_url"] = "https://tpc.googlesyndication.com/simgad/2158917315573295416"
        if self.user:
            data['user'] = self.user.get_data()
            pass
        return data

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = core_util.get_current_time()
        return super(Post, self).save(*args, **kwargs)


class Secret(models.Model):
    id = models.CharField(max_length=255, primary_key=True, db_index=True)
    push_key = models.TextField(max_length=1000, blank=True)
    device_id = models.CharField(max_length=500, blank=True)
    client_type = models.CharField(max_length=100, blank=True)
    expiry = models.DateTimeField(blank=False, null=False)
    user = models.ForeignKey(User, related_name='secrets', related_query_name='secret', on_delete=models.CASCADE)

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Secret"
        verbose_name_plural = "Secrets"

    def __str__(self):
        return "%s" % str(self.user)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = core_util.get_secret()
            self.created_at = core_util.get_current_time()
            if not self.expiry:
                self.expiry = core_util.add_time(core_const.SECRET_TTL)
        self.updated_at = core_util.get_current_time()
        return super(Secret, self).save(*args, **kwargs)
