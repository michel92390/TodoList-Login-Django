from django.shortcuts import redirect, render
# from django.http import HttpResponse
from django.views.generic.list import ListView
# for details of items
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

# to restrict the user to login first, just choose on which page you wanna do it
from django.contrib.auth.mixins import LoginRequiredMixin

# to create new users
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
 
from .models import Task

# Create your views here.
# def taskList(request):
#     return HttpResponse('to do list')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

#### DJANGO CLASS_BASED_VIEWS ####
# the 1st one for _list.html and the 2nd for _detail.html
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    # to modify the context default object_list in the loop
    context_object_name = 'tasks'

    # to see only the task of  the user log in
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # filters
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # can use title__startswith
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    # change context name instead of 'object' by default
    context_object_name = 'task'
    # change template name instead of task_detail.html
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # to redirect the user
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # to redirect the user
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')