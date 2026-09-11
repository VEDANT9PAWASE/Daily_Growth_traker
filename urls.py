from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('habits/new/', views.HabitCreateView.as_view(), name='habit_create'),
    path('habits/<int:pk>/edit/', views.HabitUpdateView.as_view(), name='habit_update'),
    path('habits/<int:pk>/delete/', views.HabitDeleteView.as_view(), name='habit_delete'),
    path('habits/<int:pk>/toggle-today/', views.toggle_today, name='toggle_today'),
    path('habits/<int:pk>/progress-note/', views.progress_note, name='progress_note'),
    path('reflection/today/', views.reflection_today, name='reflection_today'),
]
