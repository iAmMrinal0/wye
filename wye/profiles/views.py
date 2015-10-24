from django.views.generic import DetailView
from django.views.generic.list import ListView

from . import models
from wye.workshops.models import Workshop
from wye.base.constants import WorkshopStatus
from wye.organisations.models import Organisation


class ProfileView(DetailView):
    model = models.Profile
    template_name = 'profile/index.html'

    def get_context_data(self, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = models.Profile.objects.get(
            slug=slug)
        context = super(
            ProfileView, self).get_context_data(*args, **kwargs)
        return context


class UserDashboard(ListView):
    model = models.Profile
    template_name = 'profile/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        user_profile = models.Profile.objects.get(user__id=self.request.user.id)
        for each_type in user_profile.get_user_type:
            if each_type == 'Tutor':
                context['workshop_list_tutor'] = Workshop.objects.filter(
                    presenter=self.request.user, status=WorkshopStatus.REQUESTED)
            if each_type == 'Regional-Lead':
                context['workshops_accepted'] = Workshop.objects.filter(
                    status=WorkshopStatus.ACCEPTED)
                context['workshops_pending'] = Workshop.objects.filter(
                    status=WorkshopStatus.REQUESTED)
                context['interested_tutors'] = models.Profile.objects.filter(
                    usertype__slug='Tutor',
                    interested_locations__name__in=user_profile.get_interested_locations).exclude(
                    user__id=self.request.user.id).count()
                context['interested_locations'] = Organisation.objects.filter(
                    location__name__in=user_profile.get_interested_locations).count()

        return context
