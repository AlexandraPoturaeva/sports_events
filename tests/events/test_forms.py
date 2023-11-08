import pytest
from datetime import date, timedelta


@pytest.mark.django_db
def test__create_event_form__with_valid_data(
        create_image,
        get_valid_data_for_create_event_form,
):
    from events.forms import CreateEventForm

    form = CreateEventForm(
        get_valid_data_for_create_event_form,
        {'logo': create_image},
    )
    assert form.is_valid()


@pytest.mark.django_db
def test__create_event_form__wrong_date_start(
        create_image,
        get_valid_data_for_create_event_form,
):
    from events.forms import CreateEventForm

    data = get_valid_data_for_create_event_form
    data['date_start'] = date.today() - timedelta(days=1)
    form = CreateEventForm(data, {'logo': create_image})
    expected_error = 'Дата начала не может быть раньше сегодня'
    assert form['date_start'].errors[0] == expected_error


@pytest.mark.django_db
def test__create_event_form__wrong_date_end(
        create_image,
        get_valid_data_for_create_event_form,
):
    from events.forms import CreateEventForm

    data = get_valid_data_for_create_event_form
    data['date_end'] = date.today() - timedelta(days=1)
    form = CreateEventForm(data, {'logo': create_image})
    expected_error = 'Дата завершения не может быть раньше даты начала'
    assert form['date_end'].errors[0] == expected_error


@pytest.mark.django_db
def test__create_event_form__existed_event_name_and_date_start(
        create_image,
        create_user,
        get_valid_data_for_create_event_form,
):
    from events.models import Event
    from core.models import Region, CityOrDistrict
    from events.forms import CreateEventForm

    data_for_form = get_valid_data_for_create_event_form
    form = CreateEventForm(data_for_form, {'logo': create_image})
    expected_error = 'Событие с такими названием и датой начала ' \
                     'уже есть в календаре мероприятий'

    data_for_model = data_for_form.copy()
    region = Region.objects.create(title='title')
    city_or_district = CityOrDistrict.objects.create(
        title='title',
        region=region,
    )
    data_for_model['region'] = region
    data_for_model['city_or_district'] = city_or_district
    data_for_model['user'] = create_user()
    Event.objects.create(**data_for_model)

    assert form['title'].errors[0] == expected_error


@pytest.mark.django_db
def test__create_event_form__existed_event_name_another_date(
        create_image,
        create_user,
        get_valid_data_for_create_event_form,
):
    from events.models import Event
    from core.models import Region, CityOrDistrict
    from events.forms import CreateEventForm

    data_for_form = get_valid_data_for_create_event_form
    form = CreateEventForm(data_for_form, {'logo': create_image})

    data_for_model = data_for_form.copy()
    region = Region.objects.create(title='title')
    city_or_district = CityOrDistrict.objects.create(
        title='title',
        region=region,
    )
    data_for_model['region'] = region
    data_for_model['city_or_district'] = city_or_district
    data_for_model['user'] = create_user()
    data_for_model['date_start'] = date.today() + timedelta(days=1)
    Event.objects.create(**data_for_model)

    assert form.is_valid()
