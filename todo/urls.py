from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-task', views.add_task, name='add-task'),
    path('all-task', views.all_tasks, name='all-task'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('update-task/<int:id>', views.update_task, name='update-task'),
    path('task-detail/<int:id>', views.detail, name='task-detail'),
    path('login', views.user_login, name='login'),
    path('signup', views.sign_up, name='signup'),
    path('about', views.about, name='about'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:task_id>/',
         views.delete_task, name='delete-task'),
]
