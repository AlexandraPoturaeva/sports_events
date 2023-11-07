from django import forms
from events.models import Event
from datetime import datetime
from events.services import \
    generate_month_choices, \
    generate_region_choices, \
    generate_sport_kind_choices


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
    date_start = forms.DateTimeField(
        label='Дата начала',
        widget=forms.SelectDateWidget(attrs={'class': 'form-select'}),
        initial=datetime.today(),
    )
    date_end = forms.DateTimeField(
        label='Дата завершения',
        widget=forms.SelectDateWidget(attrs={'class': 'form-select'}),
        initial=datetime.today(),
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
