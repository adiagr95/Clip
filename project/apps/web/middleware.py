import json
import logging

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status

from conf import HTTP_LOGGING_SERVICE
from conf import SESSION_ACTIVE, DEBUG
from core.models import User
from web.views.base_view import handler404, handler500
from core.controllers import auth_ctrl

class SessionRefreshMiddleware(object):
    _initial_http_body = None

    def process_request(self, request):
        if request.method == "OPTIONS":
            return

        # if 'file' not in request.body:
        #     self._initial_http_body = request.body

        # Pass admin portal
        if request.path[:6] == '/admin':
            return

        # Pass login/logout requests
        if request.path[:22] == '/api/users/confirm_otp' or \
            request.path[:21] == '/api/users/check_auth' or \
            request.path[:17] == '/api/users/signin' or \
            request.path[:26] == '/api/users/forget_password' or \
            request.path[:17] == '/api/users/signup' or \
            request.path[:25] == '/api/users/reset_password' or \
            request.path[:23] == '/master/api/users/login':
            return

        # Pass favicon
        if request.path[:8] == '/favicon':
            return

        # Pass utility
        if request.path[:8] == '/utility':
            return

        # Pass notification
        if request.path[:13] == '/notification':
            return

        # Authenticate api requests
        if request.path[:4] == '/api':
            if not SESSION_ACTIVE:
                return
            # Exclude file access
            if request.path[-4:] in ['.pdf', '.xml'] or request.path[-5:] in ['.xlsx']:
                return
            # Check for login
            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
                try:
                    auth_data = json.loads(request.META['HTTP_AUTHORIZATION'])
                except Exception as e:
                    return JsonResponse(data={'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

                if 'user_id' in auth_data and 'secret' in auth_data:
                    data = {
                        'user_id': auth_data['user_id'],
                        'secret': auth_data['secret']
                    }
                    try:
                        auth_ctrl.check_auth(data)
                        return
                    except IntegrityError as e:
                        return JsonResponse(data={'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return JsonResponse(data={'error': "Authorization Required"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse(data={'error': "Authorization Required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate api requests
        if request.path[:11] == '/master/api':
            if not SESSION_ACTIVE:
                return
            # Exclude file access
            if request.path[-4:] in ['.pdf', '.xml', '.xlsx']:
                return
            # Check for login
            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
                try:
                    auth_data = json.loads(request.META['HTTP_AUTHORIZATION'])
                except Exception as e:
                    return JsonResponse(data={'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

                if 'user_id' in auth_data and 'secret' in auth_data:
                    data = {
                        'user_id': auth_data['user_id'],
                        'secret': auth_data['secret']
                    }
                    try:
                        master_auth_ctrl.check_auth(data)
                        return
                    except IntegrityError as e:
                        return JsonResponse(data={'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return JsonResponse(data={'error': "Authorization Required"},
                                        status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse(data={'error': "Authorization Required"},
                                    status=status.HTTP_401_UNAUTHORIZED)

    def process_response(self, request, response):
        return response
        if request.path[:11] == '/master/api':
            return response
        if response['Content-Type'] == 'application/json':
            user = None
            try:
                if request.path[:4] == '/api':
                    session_data = json.loads(request.META['HTTP_AUTHORIZATION'])
                    user = User.objects.get(id=session_data['user_id'])
            except:
                pass
            header = ""
            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
                header = request.META['HTTP_AUTHORIZATION']
            user_agent = ''
            if 'HTTP_USER_AGENT' in request.META and request.META['HTTP_USER_AGENT']:
                user_agent = str(request.META['HTTP_USER_AGENT'])
            data = {
                'request': self._initial_http_body,
                'response': response.content,
                'method': request.method,
                'header': header,
                'response_code': response.status_code,
                'url': request.get_full_path(),
                'user': user,
                'user_agent': user_agent
            }
            if HTTP_LOGGING_SERVICE:
                HttpActivity.objects.create(**data)
        return response

    def process_exception(self, request, exception):
        logging.getLogger('custom').exception(exception)
        return JsonResponse(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        # if request.META.get('HTTP_ACCEPT') == "application/json":
        #     return JsonResponse(data={'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return handler500(request)
