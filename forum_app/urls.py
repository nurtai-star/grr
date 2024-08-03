from django.urls import path
from .views import TopicListView, TopicDetailView, TopicCreateView, ProfileView

urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('topic/new/', TopicCreateView.as_view(), name='topic_create'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
