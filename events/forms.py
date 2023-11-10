from django import forms
from events.models import Event, Participant
from datetime import date
from events.services import \
    generate_month_choices, \
    generate_region_choices, \
    generate_sport_kind_choices
import re


class CreateEventForm(forms.Form):
    title = forms.CharField(
        label='Название',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    region = forms.CharField(
        label='Регион',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    city_or_district = forms.CharField(
        label='Район/город',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    latitude = forms.FloatField(
        label='Широта',
        min_value=-90.0,
        max_value=90.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    longitude = forms.FloatField(
        label='Долгота',
        min_value=-180.0,
        max_value=180.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        label='Анонс',
        max_length=255,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
    )
    event_type = forms.ChoiceField(
        label='Тип события',
        choices=Event.event_type.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    participation_type = forms.ChoiceField(
        label='Участие',
        choices=Event.participation_type.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    date_start = forms.DateField(
        label='Дата начала',
        widget=forms.SelectDateWidget(attrs={'class': 'form-select'}),
        initial=date.today(),
    )
    date_end = forms.DateField(
        label='Дата завершения',
        widget=forms.SelectDateWidget(attrs={'class': 'form-select'}),
        initial=date.today(),
    )
    sport_kind = forms.ChoiceField(
        label='Вид спорта',
        choices=Event.sport_kind.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    scale = forms.ChoiceField(
        label='Уровень',
        choices=Event.scale.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    logo = forms.ImageField(
        label='Логотип мероприятия',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )
    publication_status = forms.ChoiceField(
        label='Статус публикации',
        choices=Event.publication_status.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        date_start = cleaned_data.get('date_start')
        date_end = cleaned_data.get('date_end')

        if date_start < date.today():
            msg = 'Дата начала не может быть раньше сегодня'
            self.add_error('date_start', msg)

        if date_end < date_start:
            msg = 'Дата завершения не может быть раньше даты начала'
            self.add_error('date_end', msg)

        if Event.objects.filter(
                title=title,
                date_start=date_start,
                publication_status='PUB',
        ):
            msg = 'Событие с такими названием и датой начала ' \
                  'уже есть в календаре мероприятий'
            self.add_error('title', msg)


class FilterEventsForm(forms.Form):
    sport_kind = forms.ChoiceField(choices=generate_sport_kind_choices())
    region = forms.ChoiceField(choices=generate_region_choices())
    dates = forms.ChoiceField(choices=generate_month_choices())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].initial = 'ALL'
            self.fields[field].widget.attrs.update({'class': 'form-select'})


class SubmitApplicationForm(forms.Form):
    region = forms.CharField(
        label='Регион',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    city_or_district = forms.CharField(
        label='Район/город',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    application_type = forms.ChoiceField(
        label='Тип заявки',
        choices=[('TE', 'От команды'), ('IN', 'Лично')],
        widget=forms.RadioSelect(),
        initial='TE',
    )
    team_name = forms.CharField(
        label='Название команды',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        label='Телефон представителя',
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            msg = 'Номер телефона должен содержать от 9 до 15 цифр'
            self.add_error('phone_number', msg)
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        application_type = cleaned_data.get("application_type")
        team_name = cleaned_data.get("team_name")
        if application_type == 'TE' and not team_name:
            msg = 'Обязательное поле'
            self.add_error('team_name', msg)


class AddParticipantForm(forms.Form):
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя',
    )
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия',
    )
    third_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label='Отчество',
    )
    qualification = forms.ChoiceField(
        choices=Participant.qualification.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='IMS',
        label='Квалификация',
    )
    gender = forms.ChoiceField(
        choices=Participant.gender.field.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='M',
        label='Пол',
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        initial=date.today(),
        label='Дата рождения',
    )

    def clean_birth_date(self):
        today_date = date.today()
        today_year = today_date.year
        hundred_years_ago = today_date.replace(year=today_year-100)
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date > today_date or birth_date < hundred_years_ago:
            msg = 'Введите верную дату'
            self.add_error('birth_date', msg)

        return birth_date


AddParticipantFormset = forms.formset_factory(
    AddParticipantForm,
    extra=1,
    max_num=50,
    validate_max=True,
)
