from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_dict = { key: body[key] for key in ('username', 'first_name', 'last_name') }
        user_dict['password'] = make_password(body['password'])
        user_dict['email'] = user_dict['username']
        try:
            new_user = User(**user_dict)
            new_user.save()
            json_res = {'success': True}
            return JsonResponse(json_res)
        except Exception:
            json_res = {'success': False, 'error': 'Email already in use.'}
            return JsonResponse(json_res)


def user_login(request):
    body = json.loads(request.body)
    username, password = body['email'], body['password']
    import pdb;pdb.set_trace()
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        json_res = {'success': True}
        return JsonResponse(json_res)
    else:
        json_res = {'success': False}
        return JsonResponse(json_res)

