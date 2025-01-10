from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from base.models import Task

# Create your views here.
class Login(LoginView):
    template_name='base/login.html'
    fields= '__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks')

class Register(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(Register,self).form_valid(form)

    def get(self,*args,**kwarags):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register,self).get(*args,)

class tasklist(LoginRequiredMixin,ListView):
    model = Task 
    context_object_name='tasklist'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasklist']=context['tasklist'].filter(user=self.request.user)
        context['count']=context['tasklist'].filter(complete=False).count()
        
        search_input=self.request.GET.get('search-area')or ''

        if search_input:
            context['tasklist']=context['tasklist'].filter(title__icontains= search_input)
        
        context['search']=search_input

        return context

class detaialView(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')

    