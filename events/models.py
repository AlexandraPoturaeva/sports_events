from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from core.models import TimeStampedModel
from core.services import get_sentinel_user


class Event(TimeStampedModel):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at', 'title']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    title = models.CharField(max_length=100)
    region = models.ForeignKey(
        'core.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city_or_district = models.ForeignKey(
        'core.CityOrDistrict',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
    )
    description = models.CharField(max_length=255)
    event_type = models.CharField(
        max_length=2,
        choices=[
            ('CO', 'Соревнования'),
            ('TC', 'Тренировочные сборы'),
            ('SE', 'Семинар'),
        ],
    )
    participation_type = models.CharField(
        max_length=2,
        choices=[
            ('IN', 'Индивидуальные'),
            ('TE', 'Командные или эстафетные'),
        ],
    )
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    sport_kind = models.CharField(
        max_length=4,
        choices=[
            ('ORI', 'Ориентирование'),
            ('ROG', 'Рогейн'),
            ('RUN', 'Бег, трейл, скайраннинг, ходьба'),
            ('ADV', 'Гонки приключенческие, с препятствиями'),
            ('ALP', 'Туризм, скалолазание, альпинизм'),
            ('BYC', 'Велоспорт'),
            ('SKI', 'Лыжные гонки, лыжероллеры'),
            ('MULT', 'Триатлон, дуатлон, swimrun'),
            ('SWIM', 'Плавание'),
            ('OTH', 'Прочее'),
        ],
    )
    scale = models.CharField(
        max_length=4,
        choices=[
            ('TR', 'Тренировочные'),
            ('LOC', 'Локальные'),
            ('REG', 'Региональные'),
            ('IREG', 'Межрегиональные (зональные)'),
            ('NAT', 'Национальные'),
            ('INT', 'Международные'),
        ],
    )
    logo = models.ImageField(upload_to='event_logos')
    publication_status = models.CharField(
        max_length=3,
        choices=[
            ('DR', 'Черновик'),
            ('PUB', 'Опубликовано'),
            ('NS', 'Не показывать в календаре'),
        ],
    )

    def __str__(self):
        return self.title
