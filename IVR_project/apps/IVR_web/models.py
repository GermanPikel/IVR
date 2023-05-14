from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Timeline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фотография')
    DAY = [
        (0, 'Не выбран'),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31)
    ]
    MONTH = [
        (0, 'Не выбран'),
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь'),
        (11, 'Ноябрь'),
        (12, 'Декабрь'),
    ]
    day_start = models.IntegerField(null=False, blank=False, choices=DAY, verbose_name='День начала')
    month_start = models.IntegerField(null=False, blank=False, choices=MONTH, verbose_name='Месяц начала')
    year_start = models.IntegerField(null=False, blank=False, verbose_name='Год начала')
    day_end = models.IntegerField(null=False, blank=False, choices=DAY, verbose_name='День окончания')
    month_end = models.IntegerField(null=False, blank=False, choices=MONTH, verbose_name='Месяц окончания')
    year_end = models.IntegerField(null=True, blank=True, verbose_name='Год окончания')
    content = models.TextField(null=False, blank=False, verbose_name='Описание')
    is_private = models.BooleanField(default=False, verbose_name='Приватный тайм-лайн')
    time_create = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Время редактирования')

    class Meta:
        verbose_name = 'Тайм-лайн'
        verbose_name_plural = 'Тайм-лайны'

    def is_vis(self):
        if self.year_start % 4 == 0:
            return 1
        return 0

    def get_month_days(self, pos):
        if pos == 'start':
            if self.month_start in [1, 3, 5, 7, 8, 10, 12]:
                return 31 * self.month_start
            elif self.month_start in [4, 6, 9, 11]:
                return 30 * self.month_start
            return (self.is_vis() + 28) * self.month_start
        else:
            if self.month_end in [1, 3, 5, 7, 8, 10, 12]:
                return 31 * self.month_end
            elif self.month_end in [4, 6, 9, 11]:
                return 30 * self.month_end
            return (self.is_vis() + 28) * self.month_end

    def __lt__(self, other):
        return (int(self.year_start) * (365 + self.is_vis()) + int(self.get_month_days('start')) + int(
            self.day_start)) < (
                           int(other.year_start) * (365 + self.is_vis()) + int(other.get_month_days('start')) + int(
                       other.day_start))

    def get_num_start(self):
        return (int(self.year_start) * (365) + int(self.get_month_days('start')) + int(
            self.day_start))

    def get_num_end(self):
        return (int(self.year_end) * (365) + int(self.get_month_days('end')) + int(
            self.day_end))

    def __get_month_start(self):
        if self.month_start == 0:
            return ''
        elif int(self.month_start) == 1:
            if int(self.day_start):
                return 'Января'
            return 'Январь'
        elif int(self.month_start) == 2:
            if int(self.day_start):
                return 'Февраля'
            return 'Февраль'
        elif int(self.month_start) == 3:
            if int(self.day_start):
                return 'Марта'
            return 'Март'
        elif int(self.month_start) == 4:
            if int(self.day_start):
                return 'Апреля'
            return 'Апрель'
        elif int(self.month_start) == 5:
            if int(self.day_start):
                return 'Мая'
            return 'Май'
        elif int(self.month_start) == 6:
            if int(self.day_start):
                return 'Июня'
            return 'Июнь'
        elif int(self.month_start) == 7:
            if int(self.day_start):
                return 'Июля'
            return 'Июль'
        elif int(self.month_start) == 8:
            if int(self.day_start):
                return 'Августа'
            return 'Август'
        elif int(self.month_start) == 9:
            if int(self.day_start):
                return 'Сентября'
            return 'Сентябрь'
        elif int(self.month_start) == 10:
            if int(self.day_start):
                return 'Октября'
            return 'Октябрь'
        elif int(self.month_start) == 11:
            if int(self.day_start):
                return 'Ноября'
            return 'Ноябрь'
        elif int(self.month_start) == 12:
            if int(self.day_start):
                return 'Декабря'
            return 'Декабрь'

    def __get_month_end(self):
        if self.month_end == 0:
            return ''
        elif int(self.month_end) == 1:
            if int(self.day_end):
                return 'Января'
            return 'Январь'
        elif int(self.month_end) == 2:
            if int(self.day_end):
                return 'Февраля'
            return 'Февраль'
        elif int(self.month_end) == 3:
            if int(self.day_end):
                return 'Марта'
            return 'Март'
        elif int(self.month_end) == 4:
            if int(self.day_end):
                return 'Апреля'
            return 'Апрель'
        elif int(self.month_end) == 5:
            if int(self.day_end):
                return 'Мая'
            return 'Май'
        elif int(self.month_end) == 6:
            if int(self.day_end):
                return 'Июня'
            return 'Июнь'
        elif int(self.month_end) == 7:
            if int(self.day_end):
                return 'Июля'
            return 'Июль'
        elif int(self.month_end) == 8:
            if int(self.day_end):
                return 'Августа'
            return 'Август'
        elif int(self.month_end) == 9:
            if int(self.day_end):
                return 'Сентября'
            return 'Сентябрь'
        elif int(self.month_end) == 10:
            if int(self.day_end):
                return 'Октября'
            return 'Октябрь'
        elif int(self.month_end) == 11:
            if int(self.day_end):
                return 'Ноября'
            return 'Ноябрь'
        elif int(self.month_end) == 12:
            if int(self.day_end):
                return 'Декабря'
            return 'Декабрь'

    def __get_date(self, position):
        if position == 'start':
            if self.month_start:
                if self.day_start:
                    return str(self.day_start) + ' ' + self.__get_month_start()
                else:
                    return self.__get_month_start()
            else:
                return ''
        else:
            if self.month_end:
                if self.day_end:
                    return str(self.day_end) + ' ' + self.__get_month_end()
                else:
                    return self.__get_month_end()
            else:
                return ''

    def date_start(self):
        return self.__get_date('start') + ' ' + str(self.year_start)

    def date_end(self):
        if self.year_end == 72766797:
            return 'Наше время'
        return self.__get_date('end') + ' ' + str(self.year_end)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timeline', kwargs={'timeline_id': self.pk})


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeline = models.ForeignKey('Timeline', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Название')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    DAY = [
        (0, 'Не выбран'),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31)
    ]
    MONTH = [
        (0, 'Не выбран'),
        (1, 'Январь'),
        (2, 'Февраль'),
        (3, 'Март'),
        (4, 'Апрель'),
        (5, 'Май'),
        (6, 'Июнь'),
        (7, 'Июль'),
        (8, 'Август'),
        (9, 'Сентябрь'),
        (10, 'Октябрь'),
        (11, 'Ноябрь'),
        (12, 'Декабрь'),
    ]
    day_start = models.IntegerField(null=False, blank=False, choices=DAY, verbose_name='День начала')
    month_start = models.IntegerField(null=False, blank=False, choices=MONTH, verbose_name='Месяц начала')
    year_start = models.IntegerField(null=False, blank=False, verbose_name='Год начала')
    day_end = models.IntegerField(null=False, blank=False, choices=DAY, verbose_name='День окончания')
    month_end = models.IntegerField(null=False, blank=False, choices=MONTH, verbose_name='Месяц окончания')
    year_end = models.IntegerField(null=True, blank=True, verbose_name='Год окончания')
    content = models.TextField(null=False, blank=False, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Время редактирования')

    class Meta:
        verbose_name = 'Историческое событие'
        verbose_name_plural = 'Исторические события'

    def is_vis(self):
        if self.year_start % 4 == 0:
            return 1
        return 0

    def get_month_days(self, pos):
        if pos == 'start':
            if self.month_start in [1, 3, 5, 7, 8, 10, 12]:
                return 31 * self.month_start
            elif self.month_start in [4, 6, 9, 11]:
                return 30 * self.month_start
            return (self.is_vis() + 28) * self.month_start
        else:
            if self.month_end in [1, 3, 5, 7, 8, 10, 12]:
                return 31 * self.month_start
            elif self.month_end in [4, 6, 9, 11]:
                return 30 * self.month_start
            return (self.is_vis() + 28) * self.month_start

    def __lt__(self, other):
        return (int(self.year_start) * (365) + int(self.get_month_days('start')) + int(
            self.day_start)) < (
                       int(other.year_start) * (365) + int(other.get_month_days('start')) + int(
                   other.day_start))

    def __get_month_start(self):
        if self.month_start == 0:
            return ''
        elif int(self.month_start) == 1:
            if int(self.day_start):
                return 'Января'
            return 'Январь'
        elif int(self.month_start) == 2:
            if int(self.day_start):
                return 'Февраля'
            return 'Февраль'
        elif int(self.month_start) == 3:
            if int(self.day_start):
                return 'Марта'
            return 'Март'
        elif int(self.month_start) == 4:
            if int(self.day_start):
                return 'Апреля'
            return 'Апрель'
        elif int(self.month_start) == 5:
            if int(self.day_start):
                return 'Мая'
            return 'Май'
        elif int(self.month_start) == 6:
            if int(self.day_start):
                return 'Июня'
            return 'Июнь'
        elif int(self.month_start) == 7:
            if int(self.day_start):
                return 'Июля'
            return 'Июль'
        elif int(self.month_start) == 8:
            if int(self.day_start):
                return 'Августа'
            return 'Август'
        elif int(self.month_start) == 9:
            if int(self.day_start):
                return 'Сентября'
            return 'Сентябрь'
        elif int(self.month_start) == 10:
            if int(self.day_start):
                return 'Октября'
            return 'Октябрь'
        elif int(self.month_start) == 11:
            if int(self.day_start):
                return 'Ноября'
            return 'Ноябрь'
        elif int(self.month_start) == 12:
            if int(self.day_start):
                return 'Декабря'
            return 'Декабрь'

    def __get_month_end(self):
        if self.month_end == 0:
            return ''
        elif int(self.month_end) == 1:
            if int(self.day_end):
                return 'Января'
            return 'Январь'
        elif int(self.month_end) == 2:
            if int(self.day_end):
                return 'Февраля'
            return 'Февраль'
        elif int(self.month_end) == 3:
            if int(self.day_end):
                return 'Марта'
            return 'Март'
        elif int(self.month_end) == 4:
            if int(self.day_end):
                return 'Апреля'
            return 'Апрель'
        elif int(self.month_end) == 5:
            if int(self.day_end):
                return 'Мая'
            return 'Май'
        elif int(self.month_end) == 6:
            if int(self.day_end):
                return 'Июня'
            return 'Июнь'
        elif int(self.month_end) == 7:
            if int(self.day_end):
                return 'Июля'
            return 'Июль'
        elif int(self.month_end) == 8:
            if int(self.day_end):
                return 'Августа'
            return 'Август'
        elif int(self.month_end) == 9:
            if int(self.day_end):
                return 'Сентября'
            return 'Сентябрь'
        elif int(self.month_end) == 10:
            if int(self.day_end):
                return 'Октября'
            return 'Октябрь'
        elif int(self.month_end) == 11:
            if int(self.day_end):
                return 'Ноября'
            return 'Ноябрь'
        elif int(self.month_end) == 12:
            if int(self.day_end):
                return 'Декабря'
            return 'Декабрь'

    def __get_date(self, position):
        if self.year_end == 72766797:
            self.year_end = self.year_start
        if position == 'start':
            if self.month_start:
                if self.day_start:
                    return str(self.day_start) + ' ' + self.__get_month_start()
                else:
                    return self.__get_month_start()
            else:
                return ''
        else:
            if self.month_end:
                if self.day_end:
                    return str(self.day_end) + ' ' + self.__get_month_end()
                else:
                    return self.__get_month_end()
            else:
                return ''

    def date_start(self):
        if self.year_end == 72766797:
            self.year_end = self.year_start
        return self.__get_date('start') + ' ' + str(self.year_start)

    def date_end(self):
        if self.year_end == 72766797:
            self.year_end = self.year_start
            return None
        return self.__get_date('end') + ' ' + str(self.year_end)

    def __str__(self):
        return self.name

    def get_num_start(self):
        return (int(self.year_start) * (365) + int(self.get_month_days('start')) + int(
            self.day_start))

    def get_num_end(self):
        return (int(self.year_end) * (365) + int(self.get_month_days('end')) + int(
            self.day_end))

    def get_absolute_url(self):
        return reverse('event', kwargs={'event_id': self.pk})
