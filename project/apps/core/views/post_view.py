from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import Post, User
from core.controllers import post_ctrl

@api_view(['GET', 'POST'])
def posts(request, pk):
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return JsonResponse(data={'error': "User doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        if 'skip' in request.GET and request.GET['skip']:
            skip = int(request.GET['skip'])
            posts = Post.objects.all().order_by('-created_at')[skip:skip + 10]
        else:
            posts = Post.objects.all().order_by('-created_at')[:10]
        response = [p.get_data() for p in posts]
        return JsonResponse(data={'data': response}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if 'title' in request.data:
            try:
                with transaction.atomic():
                    post_data = request.data
                    post_data["user"] = user
                    post_data["file"] = request.FILES
                    post = post_ctrl.create_post(post_data)
                    return JsonResponse(data={'data': post.get_data()}, status=status.HTTP_200_OK)
            except IntegrityError as e :
                return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={'error': "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
