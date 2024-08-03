from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Topic, Comment
from .forms import TopicForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class TopicListView(ListView):
    model = Topic
    template_name = 'topic_list.html'
    context_object_name = 'topics'
    ordering = ['-created_at']
    paginate_by = 5

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(topic=self.object).order_by('created_at')
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.topic = self.object
                comment.save()
                return self.get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topic_form.html'
    success_url = reverse_lazy('topic_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'profile.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['comments_count'] = Comment.objects.filter(author=self.request.user).count()
        return context
