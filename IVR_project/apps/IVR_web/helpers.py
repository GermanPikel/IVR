from django.conf import settings
from django.core.mail import send_mail

from IVR_project.apps.IVR_web.models import Timeline


def day_to_num(day: str) -> int:
    if day == 'Не выбран':
        return 0
    return int(day)


def num_to_day(day: int) -> str:
    day = int(day)
    if day == 0:
        return 'Не выбран'
    return str(day)


def num_to_month(month: int) -> str:
    month = int(month)
    months = Timeline.MONTH
    for i in range(len(months)):
        if months[i][0] == month:
            return months[i][1]


def month_to_num(month: str) -> int:
    months = Timeline.MONTH
    for i in range(len(months)):
        if months[i][1] == month:
            return months[i][0]


def send_feedback(email, theme, message):
    control_message = email + ': ' + message
    send_mail(theme,
              control_message,
              settings.DEFAULT_FROM_EMAIL,
              [settings.EMAIL_HOST_USER],
              fail_silently=False)