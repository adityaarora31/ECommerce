from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserEmailForm


def register_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_dict = { key: body[key] for key in ('username', 'first_name', 'last_name') }
        user_dict.update({
            'password': make_password(body['password']), 
            'email': user_dict['username'],
            'is_active': False
        })

        try:
            new_user = User(**user_dict)
            new_user.save()
            
            url = f"http://127.0.0.1:8000/api/user/verify/{new_user.password.replace('/','*')}"
            full_name = f'{new_user.first_name} {new_user.last_name}'
            context = {'action': 'Confirm Email', 'url': url, 'full_name': full_name}
            html_message = render_to_string('master/email.html', context)
            plain_message = strip_tags(html_message)
            send_mail('Best Store Account Confirmation', plain_message, 'yamalik42@gmail.com', [new_user.email], html_message=html_message, fail_silently=False,)
            
            json_res = {'success': True}
            return JsonResponse(json_res)
        except Exception:
            json_res = {'success': False, 'error': 'Email already in use.'}
            return JsonResponse(json_res)


def user_login(request):
    body = json.loads(request.body)
    username, password = body['email'], body['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        name = user.first_name
        request.session['username'] = name
        login(request, user)
        json_res = {'success': True}
        return JsonResponse(json_res)
    else:
        json_res = {'success': False}
        return JsonResponse(json_res)


def verify_user(request, token):
    user = User.objects.get(password=token.replace("*", "/"))
    if user is not None:
        user.is_active = True
        user.save()
        return redirect('/')
    else:
        import pdb;pdb.set_trace()


def logout_view(request):
    logout(request)
    return redirect("homepage")


def user_dashboard(request):
    return render(request, "user_master/dashboard.html")


def forgot_pass(request):
    form = UserEmailForm(request.POST)
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)

            # import pdb;    pdb.set_trace()

            url = f"http://127.0.0.1:8000/password-reset-confirm/'{uidb64.token.replace('<uidb64>','<token>')}"
            context = {'action': 'Reset Password', 'url': url,}
            html_message = render_to_string('master/password_reset_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail('Best Store Account Confirmation', plain_message, 'yamalik42@gmail.com', [email], html_message=html_message, fail_silently=False, )
            return HttpResponseRedirect('/password-reset/done/')

        else:
            form = UserEmailForm()
    return render(request, 'test.html', {'form': form})
