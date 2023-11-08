from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


def test__create_event_view__redirect_unlogged_user_to_login(client):
    url = reverse('create_event')
    response = client.get(url)
    assert response.status_code == 302
    assert response['Location'] == reverse('login') + '?next=/events/create/'


def test__create_event_view__status_code_ok_for_logged_in_user(auto_login_user):
    client, user = auto_login_user()
    url = reverse('create_event')
    response = client.get(url)
    assert response.status_code == 200


def test__create_event_view__uses_correct_template(auto_login_user):
    client, user = auto_login_user()
    url = reverse('create_event')
    response = client.get(url)
    assertTemplateUsed(response=response, template_name='create_event.html')


def test__create_event_view__template_context_includes_correct_form(auto_login_user):
    from events.forms import CreateEventForm

    client, user = auto_login_user()
    url = reverse('create_event')
    response = client.get(url)

    assert isinstance(response.context['form'], CreateEventForm)
