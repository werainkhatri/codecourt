from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register_n'),
    path('login/', views.login, name='login_n'),
    path('logout/', views.logout, name='logout_n'),
    path('submissions/', views.submissions, name='submissions'),
]
