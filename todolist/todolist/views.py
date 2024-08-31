from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import context



def task_list(request):
    return render(request, 'todolist/task_list.html')


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Task, Category
from .forms import TaskForm


class TaskListView(DetailView):
    model = Task
    template_name = 'todolist/task_list.html'
    context_object_name = 'task_list'



class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')


class TaskDetailView:
    pass