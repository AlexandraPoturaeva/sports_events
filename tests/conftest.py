import pytest
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


@pytest.fixture
def test_password():
    return 'test_password'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def create_user_function(test_email='test@example.com'):
        return django_user_model.objects.create_user(
            email=test_email,
            password=test_password,
        )

    return create_user_function


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def auto_login_user_function(user=None):
        if user is None:
            user = create_user()
        client.login(email=user.email, password=test_password)
        return client, user

    return auto_login_user_function


@pytest.fixture
def create_image():
    f = BytesIO()
    image = Image.new(mode='RGB', size=(100, 100))
    image.save(f, 'JPEG')
    test_image = SimpleUploadedFile(
        name="test_image.jpg",
        content=f.getvalue(),
        content_type='image/jpeg',
    )
    return test_image


@pytest.fixture
def get_valid_data_for_create_event_form():
    return {
        'title': 'Название мероприятия',
        'region': 'Название региона',
        'city_or_district': 'Название города',
        'latitude': 55.755811,
        'longitude': 37.617617,
        'description': 'Описание мероприятия',
        'event_type': 'CO',
        'participation_type': 'IN',
        'date_start': date.today(),
        'date_end': date.today(),
        'sport_kind': 'ORI',
        'scale': 'LOC',
        'publication_status': 'PUB',
    }
