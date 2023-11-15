from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView, View
from events.forms import \
    CreateEventForm, \
    SubmitApplicationForm, \
    AddParticipantFormset
from django.http import HttpResponseRedirect
from core.models import Region, CityOrDistrict
from events.models import Event, Application, Participant


class CreateEventView(LoginRequiredMixin, FormView):
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


class SubmitApplicationView(LoginRequiredMixin, TemplateView):
    template_name = 'submit_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_form'] = SubmitApplicationForm(
            self.request.POST or None,
        )
        context['add_participant_formset'] = AddParticipantFormset(
            self.request.POST or None,
            prefix='add-participant',
        )
        return context

    def post(self, request, event_id, *args, **kwargs):
        application_form = SubmitApplicationForm(request.POST)
        participant_formset = AddParticipantFormset(
            request.POST,
            prefix='add-participant',
        )

        if not (
            application_form.is_valid() and
            participant_formset.is_valid()
        ):
            return self.render_to_response(self.get_context_data())

        application_data = application_form.cleaned_data

        region, created = Region.objects.get_or_create(
            title=application_data.get('region'),
        )
        city_or_district, created = CityOrDistrict.objects.get_or_create(
            title=application_data.get('city_or_district'),
            region=region,
        )

        application_data['user'] = self.request.user
        application_data['event'] = Event.objects.get(pk=event_id)
        application_data['region'] = region
        application_data['city_or_district'] = city_or_district
        application_data['is_team'] = False

        if application_data.pop('application_type') == 'TE':
            application_data['is_team'] = True

        application_obj = Application.objects.create(**application_data)

        for participant_data in participant_formset.cleaned_data:
            participant_data['application'] = application_obj
            Participant.objects.create(**participant_data)

        success_url = reverse('event_details', kwargs={'event_id': event_id})
        return HttpResponseRedirect(success_url)


class EventDetailView(View):
    def get(self, request, event_id):
        participants = Participant.objects.filter(
            application__event__pk=event_id,
        )
        context = {
            'event': get_object_or_404(Event, pk=event_id),
            'participants': participants,
        }
        return render(request, 'event.html', context=context)
