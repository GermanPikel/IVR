import os

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

from IVR_project.apps.IVR_web.helpers import *
from IVR_project.apps.IVR_web.models import *
from IVR_project.apps.IVR_web.forms import *


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h2>страница не найдена(((</h2>')  # будет работать только при DEBUG=False


def main_page(request):
    user = User.objects.get(username='admin')
    user_ident = user.pk
    timelines = sorted(Timeline.objects.filter(user=user_ident, is_private=0))
    context = {
        'timelines': timelines
    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)

    return render(request, 'main_page.html', context)


def main_page_detailed(request):
    user = User.objects.get(username='admin')
    user_ident = user.pk
    public_timelines = sorted(Timeline.objects.filter(user=user_ident, is_private=0))
    evs = []
    for i in public_timelines:
        pr_key = i.pk
        events = Event.objects.filter(user=user_ident, timeline=pr_key)
        evs += events

    timelines = sorted(evs)
    context = {
        'timelines': timelines
    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    if request.method == 'POST':
        email = request.POST.get('email')
        message = email + ': ' + request.POST.get('message')
        theme = request.POST.get('theme')
        if True:
            send_mail(theme,
                      message,
                      settings.DEFAULT_FROM_EMAIL,
                      [settings.EMAIL_HOST_USER],
                      fail_silently=False)

    return render(request, 'main_page.html', context)


def open_login(request):
    return render(request, 'login.html', context={})


def login_(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
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
    if tl.is_private:
        if request.user != tl.user:
            raise Http404()
    tl_master = tl.user
    events = sorted(Event.objects.filter(timeline_id=timeline_id))
    context = {
        'tl': tl,
        'events': events
    }
    if request.user.is_authenticated:
        context['user_'] = request.user
    if request.user == tl_master:
        context['master'] = True
    else:
        context['master'] = False
    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)
    return render(request, 'timeline.html', context)


def open_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    tl_pk = event.timeline.pk
    tl = Timeline.objects.get(pk=tl_pk)
    if tl.is_private:
        if request.user != event.user:
            raise Http404()
    tl_master = event.user
    context = {
        'event': event
    }
    if request.user.is_authenticated:
        context['user_'] = request.user
    if request.user == tl_master:
        context['master'] = True
    else:
        context['master'] = False
    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)
    return render(request, 'event.html', context)


def profile(request, username):
    user_ = User.objects.get(username=username)
    context = {}
    if user_ == request.user:
        context['redact_rules'] = True
        watch_private = True
    else:
        context['redact_rules'] = False
        watch_private = False
    if watch_private:
        timelines = sorted(Timeline.objects.filter(user=user_.pk))
        timelines_total = len(timelines)
    else:
        timelines = sorted(Timeline.objects.filter(user=user_.pk, is_private=0))
        timelines_total = len(timelines)
    context['timelines'] = timelines
    context['timelines_total'] = timelines_total
    if request.user.is_authenticated:
        context['user_'] = request.user
    context['user_search'] = user_
    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)
    return render(request, 'profile.html', context)


def logout_(request):
    logout(request)
    user = User.objects.get(username='admin')
    user_ident = user.pk
    timelines = Timeline.objects.filter(user=user_ident, is_private=0)
    context = {
        'timelines': timelines,
        'user_': request.user.is_authenticated
    }
    return redirect('home', permanent=True)
    # return render(request, 'main_page.html', context)


def search_params(request):
    context = {}

    if request.user.is_authenticated:
        context['user_'] = request.user

    text = request.POST.get('text')
    parameter = request.POST.get('parameter')
    context['parameter'] = parameter
    if parameter == 'Пользователь':
        if User.objects.filter(username=text).exists():
            user_searched = User.objects.get(username=text)
            user_evs = Event.objects.filter(user=user_searched.id)
            user_tls = Timeline.objects.filter(user=user_searched.id, is_private=0)
            events_count = len(user_evs)
            timelines_count = len(user_tls)
            context['search_result'] = user_searched
            context['events_count'] = events_count
            context['timelines_count'] = timelines_count
    elif parameter == 'Событие':
        events = sorted(Event.objects.filter(name__icontains=text))
        context['search_result'] = events
    else:
        events = sorted(Event.objects.all())
        events_result = []
        if parameter == 'Год':
            if text.isdigit():
                for event in events:
                    if int(text) >= event.year_start and int(text) <= event.year_end:
                        events_result.append(event)
        else:
            events_result = Event.objects.filter(content__icontains=text)

        context['search_result'] = events_result

    return render(request, 'search_result_page.html', context)


def create_tl(request):

    def check_ev_date():
        cd = form.cleaned_data
        sd, sm, sy, ed, em, ey = cd['day_start'], cd['month_start'], cd['year_start'], cd['day_end'], cd['month_end'], cd['year_end']
        tl = Timeline.objects.get(pk=context['tl_pk'])
        te = Event.objects.create(user=request.user, timeline=tl, day_start=sd, month_start=sm, year_start=sy,
                                  day_end=ed, month_end=em, year_end=ey, content=' ',
                                  photo=' ')
        ns = tl.get_num_start()
        ne = tl.get_num_end()
        ns1 = te.get_num_start()
        ne1 = te.get_num_end()

        if (ns1 < ns or ne1 > ne):
            if ey != 72766797:
                context['date_error'] = 'Даты начала и окончания события должны соответствовать тайм-лайну'
            else:
                if ns1 < ns:
                    context['date_error'] = 'Даты начала и окончания события должны соответствовать тайм-лайну'
                else:
                    context['date_error'] = None

        else:
            context['date_error'] = None
        Event.objects.filter(pk=te.pk).delete()

    context = {}
    hidden = request.POST.get('hide')
    if request.user.is_authenticated:
        context['user_'] = request.user

    if hidden is None or hidden == 't':
        if request.method == 'POST':
            form = AddTimeline(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['year_end'] is None:
                    cd['year_end'] = 72766797
                cd['user'] = request.user
                new_tl = Timeline.objects.create(**cd)

                context['hidee'] = 'e'
                context['adding_ev'] = True
                context['tl_pk'] = new_tl.pk
                context['tl_name'] = new_tl.name
                context['tl_start'] = new_tl.date_start()
                context['tl_end'] = new_tl.date_end()
                context['tl_created'] = True
                form = AddTimeline()

        else:
            form = AddTimeline()
    else:
        sbmt = request.POST.get('sbmt')
        if 'выйти' in sbmt:
            if request.method == 'POST':
                context['tl_pk'] = request.POST.get('tl_pk')
                form = AddEvent(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    if cd['year_end'] is None:
                        cd['year_end'] = 72766797
                    cd['user'] = request.user
                    cd['timeline'] = Timeline.objects.get(pk=context['tl_pk'])

                    check_ev_date()
                    if not context['date_error']:
                        new_tl = Event.objects.create(**cd)
                        context['hidee'] = 'e'
                        context['adding_ev'] = True
                        context['tl_name'] = Timeline.objects.get(pk=context['tl_pk']).name
                        context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                        context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
                        context['tl_created'] = True
                        form = AddEvent()
                        redir = context['tl_pk']
                        return redirect(f'/timeline/{redir}')
                    else:
                        context['hidee'] = 'e'
                        context['adding_ev'] = True
                        context['tl_name'] = Timeline.objects.get(pk=context['tl_pk']).name
                        context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                        context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
                        context['tl_created'] = True
                        form = AddEvent()
                        context['form'] = form
                        return render(request, 'create_tl.html', context)

            else:
                form = AddEvent()
                context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
        else:
            if request.method == 'POST':
                context['tl_pk'] = request.POST.get('tl_pk')
                form = AddEvent(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data
                    if cd['year_end'] is None:
                        cd['year_end'] = 72766797
                    cd['user'] = request.user
                    cd['timeline'] = Timeline.objects.get(pk=context['tl_pk'])
                    check_ev_date()
                    if not context['date_error']:
                        new_tl = Event.objects.create(**cd)
                        context['hidee'] = 'e'
                        context['adding_ev'] = True
                        context['tl_name'] = Timeline.objects.get(pk=context['tl_pk']).name
                        context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                        context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
                        context['tl_created'] = True
                        form = AddEvent()
                    else:
                        context['hidee'] = 'e'
                        context['adding_ev'] = True
                        context['tl_name'] = Timeline.objects.get(pk=context['tl_pk']).name
                        context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                        context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
                        context['tl_created'] = True
                        form = AddEvent()
                        context['form'] = form
                        return render(request, 'create_tl.html', context)

            else:
                form = AddEvent()
                context['tl_start'] = Timeline.objects.get(pk=context['tl_pk']).date_start()
                context['tl_end'] = Timeline.objects.get(pk=context['tl_pk']).date_end()
                context['adding_ev'] = True
                context['tl_created'] = True
                context['hidee'] = 'e'

    context['form'] = form
    return render(request, 'create_tl.html', context)


@login_required(login_url=reverse_lazy('login'))
def copy(request):
    copied_pk = request.POST.get('hide')
    copied_tl = Timeline.objects.get(pk=copied_pk)
    copied_events = Event.objects.filter(timeline=copied_pk)
    q = copied_tl.__dict__
    q['user'] = request.user
    del q['_state']
    del q['user_id']
    del q['id']
    new_tl = Timeline.objects.create(**q)
    new_pk = new_tl.pk
    for event in copied_events:
        q = event.__dict__
        if q['_state']:
            del q['_state']
        del q['user_id']
        del q['id']
        del q['timeline_id']
        q['timeline'] = new_tl
        q['user'] = request.user
        Event.objects.create(**q)
    return redirect(f'/timeline/{copied_pk}')


def redact(request):
    te = request.POST.get('te')
    pk = request.POST.get('hide')
    action = request.POST.get('smbt')
    try:
        t_pk = request.POST.get('t_pk')
    except:
        pass
    master = request.user
    master = master.username
    if action == 'Удалить':
        if te == 'e':
            Event.objects.get(pk=pk).delete()
            tl = Timeline.objects.get(user=request.user, name=t_pk).pk
            return redirect(f'/timeline/{tl}')
        else:
            Timeline.objects.get(pk=pk).delete()
            return redirect(f'/users/{master}')
    elif action == 'Редактировать':
        context = {}
        days, months = [], []
        for i in range(len(Timeline.DAY)):
            days.append(Timeline.DAY[i][1])
        for i in range(len(Timeline.MONTH)):
            months.append(Timeline.MONTH[i][1])
        context = {'months': months, 'days': days, 'user_': request.user}
        if te == 't':
            context['redact_tl'] = True
            tl = Timeline.objects.get(pk=pk)
            context['tl_pk'] = tl.pk
            context['name'] = tl.name
            context['day_start'] = num_to_day(tl.day_start)
            context['month_start'] = num_to_month(tl.month_start)
            context['year_start'] = int(tl.year_start)
            context['day_end'] = num_to_day(tl.day_end)
            context['month_end'] = num_to_month(tl.month_end)
            context['year_end'] = int(tl.year_end)
            context['photo_url'] = tl.photo.url
            context['content'] = tl.content
            context['is_private'] = tl.is_private

        else:
            context['redact_tl'] = False
            ev = Event.objects.get(pk=pk)
            context['ev_pk'] = ev.pk
            context['name'] = ev.name
            context['day_start'] = num_to_day(ev.day_start)
            context['month_start'] = num_to_month(ev.month_start)
            context['year_start'] = int(ev.year_start)
            context['day_end'] = num_to_day(ev.day_end)
            context['month_end'] = num_to_month(ev.month_end)
            context['year_end'] = int(ev.year_end)
            context['photo_url'] = ev.photo.url
            context['content'] = ev.content
    else:
        context = {
            'adding_ev': True,
        }
        tl = Timeline.objects.get(pk=pk)
        context['tl_pk'] = tl.pk
        context['tl_name'] = tl.name
        context['hidee'] = 'e'
        form = AddEvent()
        context['form'] = form
        context['tl_start'] = tl.date_start()
        context['tl_end'] = tl.date_end()
        context['user_'] = request.user
        return render(request, 'create_tl.html', context)

    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)

    return render(request, 'redact_page.html', context)


def edit(request):

    if request.POST.get('message'):
        email = request.POST.get('email')
        theme = request.POST.get('theme')
        message = request.POST.get('message')
        send_feedback(email, theme, message)

    pk_to = request.POST.get('_pk')
    t_e = request.POST.get('t_e')
    if t_e == 't':
        tl = Timeline.objects.get(user=request.user, pk=pk_to)
        if request.method == "POST":
            if len(request.FILES) != 0:
                tl.photo = request.FILES.get('photo')
            tl.name = request.POST.get('name')
            tl.day_start = day_to_num(request.POST.get('day_start'))
            tl.month_start = month_to_num(request.POST.get('month_start'))
            tl.year_start = int(request.POST.get('year_start'))
            tl.day_end = day_to_num(request.POST.get('day_end'))
            tl.month_end = month_to_num(request.POST.get('month_end'))
            tl.year_end = int(request.POST.get('year_end'))
            tl.content = request.POST.get('content')
            tl.save()
            return redirect(f'{tl.get_absolute_url()}')
    else:
        if request.method == "POST":
            pk_ev = int(request.POST.get('_pk'))
            ev = Event.objects.get(pk=pk_ev)
            if len(request.FILES) != 0:
                ev.photo = request.FILES.get('photo')
            ev.name = request.POST.get('name')
            ev.day_start = day_to_num(request.POST.get('day_start'))
            ev.month_start = month_to_num(request.POST.get('month_start'))
            ev.year_start = int(request.POST.get('year_start'))
            ev.day_end = day_to_num(request.POST.get('day_end'))
            ev.month_end = month_to_num(request.POST.get('month_end'))
            ev.year_end = int(request.POST.get('year_end'))
            ev.content = request.POST.get('content')
            ev.save()
            return redirect(f'{ev.get_absolute_url()}')
    return HttpResponse(f'{pk_to, t_e}')


def to_merge(request):
    context = {

    }
    if request.user.is_authenticated:
        context['user_'] = request.user

    timelines = Timeline.objects.filter(user=request.user)
    context['timelines'] = timelines

    return render(request, 'merge.html', context)


def merging(request):
    context = {'user_': request.user}
    name = request.POST.get('name')
    content = request.POST.get('content')
    context['name'] = name
    context['content'] = content
    context['timelines'] = Timeline.objects.filter(user=request.user)
    tls_to_merge = request.POST.getlist('to_merge')
    if name == '' or content == '' or len(request.FILES) == 0:
        context['error'] = 'Заполните все обязательные поля'
        return render(request, 'merge.html', context)
    if len(tls_to_merge) == 0:
        context['error'] = 'Выберите тайм-лайны для слияния'
        return render(request, 'merge.html', context)
    merged_events = []
    tls = []
    for i in tls_to_merge:
        tls.append(Timeline.objects.get(pk=int(i)))
    tls = sorted(tls)
    first_tl = tls[0]
    last_tl = tls[-1]
    merged_tl = Timeline.objects.create(name=name, photo=request.FILES.get('photo'), day_start=first_tl.day_start,
                                        month_start=first_tl.month_start, year_start=first_tl.year_start,
                                        day_end=last_tl.day_end, month_end=last_tl.month_end,
                                        year_end=last_tl.year_end, content=content, user=request.user, is_private=False)
    merged_pk = merged_tl.pk
    for i in tls_to_merge:
        evs = Event.objects.filter(timeline=Timeline.objects.get(pk=int(i)))
        for ev in evs:
            new_ev = Event.objects.create(name=ev.name,photo=ev.photo, day_start=ev.day_start,
                                        month_start=ev.month_start, year_start=ev.year_start,
                                        day_end=ev.day_end, month_end=ev.month_end,
                                        year_end=ev.year_end, content=content, user=request.user, timeline=merged_tl)
    return redirect(f'{request.user.get_absolute_url()}')


def send_reset_pass(request):
    context = {

    }
    return render(request, 'reset_password.html', context)


def set_new_pass(request):
    context = {

    }
    return render(request, 'reset_new_password.html', context)
