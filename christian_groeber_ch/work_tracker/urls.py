from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('create/', views.new_project),
    path('start-working/<project_id>/', views.start_working),
    path('stop-working/', views.stop_working),
    path('edit/<project_id>/', views.edit),
    path('delete/<project_id>/', views.delete),
    path('add-description/<event_id>/', views.add_description),
    path('plan/<project_id>/', views.plan),
]
