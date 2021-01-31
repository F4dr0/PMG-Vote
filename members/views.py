import string, random

from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import *


# Create your views here.

def index(request):
    return render(request, 'members/index.html')


def check_admin(user):
    return user.is_superuser


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'members/login.html')


@user_passes_test(check_admin)
def register(request):
    form = CreateUserForm()
    form.fields['password1'].widget = forms.HiddenInput()
    form.fields['password2'].widget = forms.HiddenInput()
    if request.method == 'POST':
        password = generate_password()
        data_dic = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password1': password,
            'password2': password
        }
        form = CreateUserForm(data_dic)
        if form.is_valid():
            form.save()
            return redirect('/admin/users')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'members/admin/register.html', context)


@user_passes_test(check_admin)
def showUsers(request):
    context = {'members': User.objects.all()}
    return render(request, 'members/admin/users.html', context)


@user_passes_test(check_admin)
def userDelete(request, id):
    position = User.objects.get(pk=id)
    position.delete()
    return redirect('/admin/users')


@user_passes_test(check_admin)
def send_password(receiver, password):
    message = "Twoje hasło do konta PMG:" + password + "./n Do logowania użyj tego adresu e-mail "
    send_mail(
        'Konto PMG',  # subject
        'Twoje hasło do konta PMG:',  # message
        'michal.fadrowski.pmg@gmail.com',  # sender
        [receiver],  # reciver
    )


def generate_password(length=12):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length)) + 'A!'
