
'''
Home url patterns
'''
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('load_posts/<int:offset>/', views.load_posts, name='load_posts'),
]
