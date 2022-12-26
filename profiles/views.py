from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .forms import SettingsForm, PasswordChangeForm
from .models import FollowRelation
from post.models import Post



# Create your views here.
def settings(request):
    '''
    Settings route
    '''
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():

                if not User.objects.filter(username=form.cleaned_data.get('username')).exists() or form.cleaned_data.get('username') == user.username:
                    user.username = form.cleaned_data.get('username')
                else:
                    return render(request, 'settings.html', {'form': form, 'error_message': 'Username is already taken'})
                    
                    
                user.user_text = form.cleaned_data.get('user_text')
                user.user_profile = form.cleaned_data.get('user_picture')

                user.save(update_fields=['username', 'user_text', 'user_picture'])

                return render(request, 'settings.html', {'form': form })
            else:
                return render(request, 'settings.html', {'form': form, 'error_message': 'Invalid input'})
        else:
            return render(request, 'settings.html', {'user': {'username': user.username, 'user_text':user.user_text, 'user_picture':user.user_picture}})
    else:
        return render(request, 'index.html', {'error_message': 'You cannot access this area!'})

def change_password(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                    
                if form.cleaned_data.get('password') == form.cleaned_data.get('password_confirm'):
                    user.password = form.cleaned_data.get('password')
                    user.user_profile = form.cleaned_data.get('user_picture')
                    user.save()
                    return render(request, 'settings.html', {'user': {'username': user.username, 'user_text':user.user_text, 'user_picture':user.user_picture}})
                else:
                    return render(request, 'settings.html', {'form': form, 'error_message': 'Passwords do not match'})

            else:
                return render(request, 'settings.html', {'form': form, 'error_message': 'Invalid input'})
        else:
            return render(request, 'settings.html', {'user': {'username': user.username, 'user_text':user.user_text, 'user_picture':user.user_picture}})
    else:
        return render(request, 'index.html', {'error_message': 'You cannot access this area!'})



def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(user=user).order_by('-created_at')

    if request.user.is_authenticated and request.user != user:
        is_following = FollowRelation.objects.filter(user=request.user, followed_user=user).exists()
        return render(request, 'profile.html', {'user': user, 'is_following': is_following, 'post_list': post_list})

    return render(request, 'profile.html', {'user': {'username':user.username, 'profile_picture':user.user_picture}, 'post_list': post_list})

def profile_following(request, username):
    user = get_object_or_404(User, username=username)

    follow_list = [{'username':follow_relation.followed_user.username, 'user_picture':follow_relation.followed_user.user_picture} for follow_relation in FollowRelation.objects.filter(user=user)]

    return render(request, 'profile_follow_list.html', {'user': user, 'type':'Following', 'follow_list': follow_list})


def profile_follower(request, username):
    user = get_object_or_404(User, username=username)

    follow_list = [{'username':follow_relation.followed_user.username, 'user_picture':follow_relation.followed_user.user_picture} for follow_relation in FollowRelation.objects.filter(followed_user=user)]
    return render(request, 'profile_follow_list.html', {'user': user, 'type':'Follower', 'follow_list': follow_list})


def follow(request, username):
    user = User.objects.get(username=username)

    FollowRelation.objects.create(
        user=request.user,
        followed_user=user,
        followed_at=datetime.now()
    )
    return redirect('profile', username=username)

def unfollow(request, username):
    user = User.objects.get(username=username)
    FollowRelation.objects.filter(
        user=request.user,
        followed_user=user).delete()
    return redirect('profile', username=username)