from django.urls import path
from . import views

urlpatterns = [
    path('<int:prob_id>/', views.problem, name='problem'),
]
