from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.views import generic
from groups.models import Group, GroupMember
from . import forms

from django.shortcuts import get_object_or_404

class CreateGroup(generic.CreateView, LoginRequiredMixin):
    model = Group
    fields = ['name', 'description']
    template_name = 'group_form.html'
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={ 'slug':self.kwargs.get('slug') })


class SingleGroup(generic.DetailView):
    model = Group
    template_name = 'group_detail.html'

class ListGroups(generic.ListView):
    model = Group
    template_name = 'group_list.html'

class JoinGroup(generic.RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={ 'slug':self.kwargs.get('slug') })

    def get(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, grp=group)
        except IntegrityError:
            messages.warning(self.request, ('Already a Member !'))
        else:
            messages.success(self.request, ('Now a Member !'))

        return super().get(self.request, *args, **kwargs)

class LeaveGroup(generic.RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={ 'slug':self.kwargs.get('slug') })

    def get(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            membership = GroupMember.objects.filter(user = self.request.user, grp = group).get()
        except ObjectDoesNotExist:
            messages.warning(self.request, ('Not a Member !'))
        else:
            membership.delete()
            messages.success(self.request, ('Successfully Left the Group !'))

        return super().get(self.request, *args, **kwargs)
