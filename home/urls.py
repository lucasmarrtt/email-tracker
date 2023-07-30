from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-out/', views.sign_out, name='sign-out'),
   
]
