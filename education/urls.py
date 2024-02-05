from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import login_request, register_request



urlpatterns = [
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('submit_topic/', views.submit_topic, name ="submit_topic"),
    path('topic_submitted/<int:question_id>/', views.topic_submitted, name='topic_submitted'),
    path('submit_answer/<int:question_id>', views.submit_answer, name ='submit_answer'),
    path('logout/', LogoutView.as_view(next_page='welcome_page'), name='logout'), 
    # Add other URLs as needed
]