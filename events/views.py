from django.views.generic import FormView
from events.forms import CreateEventForm
from django.http import HttpResponseRedirect
from core.models import Region, CityOrDistrict
from events.models import Event


class CreateEventView(FormView):
    form_class = CreateEventForm
    template_name = 'create_event.html'
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        region, created = Region.objects.get_or_create(
            title=data.get('region'),
        )
        city_or_district, created = CityOrDistrict.objects.get_or_create(
            title=data.get('city_or_district'),
            region=region,
        )
        data['user'] = self.request.user
        data['region'] = region
        data['city_or_district'] = city_or_district
        Event.objects.create(**data)

        return HttpResponseRedirect(self.success_url)
