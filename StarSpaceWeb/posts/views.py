from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views import generic
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from braces.views import SelectRelatedMixin
from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

class UserPosts(generic.ListView):
    model = models.Post
    template_name = "user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except ObjectDoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(generic.DetailView):
    model = models.Post
    select_related = ['user', 'group']
    template_name = 'post_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))

class CreatePost(generic.CreateView, SelectRelatedMixin, LoginRequiredMixin):
    model = models.Post
    fields = ['title', 'message', 'group']
    template_name = 'post_form.html'

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CreateComment (generic.CreateView, SelectRelatedMixin, LoginRequiredMixin):
    model = models.Comments
    fields = ['message', 'post']
    template_name = 'comments_form.html'

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.post_user.username, 'pk':self.post} )
