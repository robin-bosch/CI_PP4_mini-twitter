
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

# handler401 = views.custom_401

urlpatterns = [
    path('', views.home, name='home'),
    # path('new_post/', views.new_post, name='new_post'),
    # path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    path('load_posts/<int:offset>/', views.load_posts, name='load_posts'),
    # path('profile/', include('profiles.urls', namespace='profiles')),
    path('profiles/', include(('profiles.urls', 'profiles'), namespace="profiles")),
    # path('login/', views.login_user, name='login'),
    # path('settings/', views.settings, name='settings'),
    # path('settings/change_password', views.change_password, name='change_password'),
    # path('profile/<str:username>/following', views.profile_following, name='profile_following'),
    # path('profile/<str:username>/follower', views.profile_follower, name='profile_follower'),
    # path('profile/<str:username>/', views.profile, name='profile'),
    # path('post/<int:post_id>', views.view_post, name='view_post'),
    # path('post/<int:post_id>/vote/<int:vote_type>', views.vote_post, name='vote_post'),
    # path('post/<int:post_id>/add_comment', views.add_comment, name='add_comment'),
    # path('comment/<int:comment_id>/edit', views.edit_comment, name='edit_comment'),
    # path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    # path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    # path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    # path('profile/<str:username>/follow/', views.follow, name='follow'),
    # path('profile/<str:username>/unfollow/', views.unfollow, name='unfollow'),
]