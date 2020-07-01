from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView
from . import forms

class SignUp(CreateView):
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'Signup.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'
