
from django.shortcuts import render
from django.views.generic import TemplateView



class HomeView(TemplateView):
    template_name = 'home.html'

    # send data to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['message'] = 'This is Home page'
        return context