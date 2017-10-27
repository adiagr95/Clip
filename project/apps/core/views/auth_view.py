from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from util import core_util
from util.constants import core_const
from core.models import User
from core.controllers import auth_ctrl, user_ctrl


@api_view(['POST'])
def signin(request):
    if 'user_name' in request.data and request.data['user_name'] and 'password' in request.data and request.data['password']:
        if User.objects.filter(user_name=request.data['user_name'], password=request.data['password']).exists():
            user = User.objects.filter(user_name=request.data['user_name'], password=request.data['password'])[0]
            try:
                data = auth_ctrl.create_session(user.id, request.data)
                return JsonResponse(data={'data': data}, status=status.HTTP_200_OK)
            except IntegrityError as e:
                return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={'error': "Invalid Username or Pasword"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={'error': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    if 'user_name' in request.data and request.data['user_name'] and 'password' in request.data and request.data['password']:
        try:
            with transaction.atomic():
                user = user_ctrl.create_user(request.data)
                data = auth_ctrl.create_session(user.id, request.data)
                return JsonResponse(data={'data': data}, status=status.HTTP_200_OK)
        except IntegrityError as e :
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data={'error': "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
