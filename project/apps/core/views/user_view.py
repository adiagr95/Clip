from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User
from core.controllers import user_ctrl
from django.db import IntegrityError, transaction

@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        response = [u.get_data() for u in users]
        return JsonResponse(data={'data': response}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def user_entity(request, pk):
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse(data={'error': "User doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return JsonResponse(data={'data': user.get_data()}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            with transaction.atomic():
                user = user_ctrl.update_user(user.id, request.data)
                if 'file' in request.FILES:
                    user_ctrl.update_image(user, request.FILES)
                return JsonResponse(data={'data': user.get_data()}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return JsonResponse(data={'error': error_msg.INVALID % "Method"}, status=status.HTTP_400_BAD_REQUEST)
