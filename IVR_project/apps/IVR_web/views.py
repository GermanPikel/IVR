from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from IVR_project.apps.IVR_web.models import *


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h2>страница не найдена(((</h2>')  # будет работать только при DEBUG=False


def main_page(request):
    timelines = sorted(Timeline.objects.filter(user=1, is_private=0))
    context = {
        'timelines': timelines
    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    return render(request, 'main_page.html', context)


def open_login(request):
    return render(request, 'login.html', context={})


def login_(request):
    print('---------------------')
    username = request.POST.get('username')
    password = request.POST.get('password')
    print('---------------------')
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.check_password(raw_password=password):
            login(request, user=user)
            return redirect('home', permanent=True)
        else:
            context = {
                'error': 'Введён неверный пароль.'
            }
    else:
        context = {
            'error': 'Такого пользователя не существует.'
        }
    return render(request, 'login.html', context)


def open_reg(request):
    return render(request, 'registration.html', context={})


def registration(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_verify = request.POST.get('password_verify')
    if password_verify == password and len(password) >= 8:
        if User.objects.filter(username=username).exists():
            context = {
                'error': 'Пользователь с таким уже существует.'
            }
        elif User.objects.filter(email=email).exists():
            context = {
                'error': 'Пользователь с таким email уже существует.'
            }
        else:
            user = User.objects.create_user(username=username, email=email
                                            , password=password)
            login(request, user)
            return redirect('home', permanent=True)
    else:
        if password_verify != password:
            context = {
                'error': 'Пароли не совпадают.'
            }
        else:
            context = {
                'error': 'Длина пароля должна быть не меньше 8 символов.'
            }
    return render(request, 'registration.html', context)


def open_tl(request, timeline_id):
    tl = Timeline.objects.get(pk=timeline_id)
    events = sorted(Event.objects.filter(timeline_id=timeline_id))
    context = {
        'tl': tl,
        'events': events
    }
    if request.user.is_authenticated:
        context['user_'] = request.user
    return render(request, 'timeline.html', context)


def open_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {
       'event': event
    }
    if request.user.is_authenticated:
        context['user_'] = request.user
    return render(request, 'event.html', context)


def profile(request):
    timelines = Timeline.objects.filter(user=request.user.pk)
    timelines_total = len(timelines)
    context = {
        'timelines': timelines,
        'timelines_total': timelines_total
    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    return render(request, 'profile.html', context)


def logout_(request):
    logout(request)
    timelines = Timeline.objects.filter(user=1, is_private=0)
    context = {
        'timelines': timelines,
        'user_': request.user.is_authenticated
    }
    return render(request, 'main_page.html', context)


def js_test(request):
    context = {

    }
    return render(request, 'js_test.html', context)


def create_tl(request):
    context = {

    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    return render(request, 'create_tl.html', context)


def create_event(request):
    context = {

    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    return render(request, 'create_event.html', context)


def merge(request):
    context = {

    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    return render(request, 'merge.html', context)


def send_reset_pass(request):
    context = {

    }
    return render(request, 'reset_password.html', context)


def set_new_pass(request):
    context = {

    }
    return render(request, 'reset_new_password.html', context)