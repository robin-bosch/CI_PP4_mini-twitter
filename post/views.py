# pylint: disable=import-error
'''
Post views
'''
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from post.forms import PostForm, CommentForm

from post.models import Post, PostComment, PostVote


# Create your views here.
def new_post(request):
    '''
    Creates a new post
    '''
    if request.method == 'POST':
        if request.user.is_authenticated:

            form = PostForm(request.POST)
            if form.is_valid():
                Post.objects.create(
                    user=request.user,
                    content=form.cleaned_data['content'],
                    created_at=datetime.now()
                )
    return redirect('home')


def view_post(request, post_id):
    '''
    Allows to view the post
    '''
    # Query for the post
    post = get_object_or_404(Post, pk=post_id)

    # Get list of comments
    comment_list = PostComment.objects.filter(post=post)

    # Comment form is that needed?
    form = CommentForm()

    # Calculate Like/Dislike ratio
    like_votes = PostVote.objects.filter(post=post, type=1).count()
    dislike_votes = PostVote.objects.filter(post=post, type=0).count()

    if like_votes + dislike_votes > 0:
        vote_ratio = (like_votes / (like_votes + dislike_votes)) * 100
    else:
        vote_ratio = 0

    # Display user vote
    if request.user.is_authenticated and PostVote.objects.filter(post=post, user=request.user).exists():
        user_vote = (
            'like'
            if PostVote.objects.get(post=post, user=request.user).type == 1
            else 'dislike'
        )

        return render(request,
                      'post/post.html',
                      {'post': post,
                       'comment_list': comment_list,
                       'vote_ratio': vote_ratio,
                       'user_vote': user_vote,
                       'form': form})

    # Render template without vote
    return render(request,
                  'post/post.html',
                  {'post': post,
                   'comment_list': comment_list,
                   'vote_ratio': vote_ratio,
                   'form': form})


def add_comment(request, post_id):
    '''
    Adds comment to post
    '''
    # Query for the post
    post = get_object_or_404(Post, pk=post_id)

    # Add a new comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                PostComment.objects.create(
                    user=request.user,
                    post=post,
                    content=form.cleaned_data['content'],
                    created_at=datetime.now()
                )
                return redirect('view_post', post_id=post.id)

    return render(request,
                  'home/index.html',
                  {'error_message': 'Invalid request'})


def edit_comment(request, comment_id):
    '''
    Edit comment route
    '''
    comment = PostComment.objects.get(id=comment_id)

    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():

                comment.content = form.cleaned_data['content']
                comment.save()
                return redirect('view_post', post_id=comment.post.id)

            return render(request,
                          'post/edit_comment.html',
                          {'form': form, 'error_message': 'Invalid input'})

        form = CommentForm(initial={'content': comment.content})
        return render(request,
                      'post/edit_comment.html',
                      {'comment': comment})

    return render(request,
                  'post/post.html',
                  {'post': comment.post,
                   'error_message': 'Really? No you cannot edit this comment, this is not your comment!'})


def delete_comment(request, comment_id):
    '''
    Deletes comment
    '''
    comment = PostComment.objects.get(id=comment_id)
    if request.user == comment.user:
        post_id = comment.post.id

        comment.delete()

        return redirect('view_post', post_id=post_id)

    return render(request,
                  'post/post.html',
                  {'post': comment.post,
                   'error_message': '''Really? No you cannot delete this
                   comment, this is not your comment!'''})


def edit_post(request, post_id):
    '''
    Edit post route
    '''
    post = Post.objects.get(id=post_id)

    if request.user == post.user:
        if request.method == 'POST':

            form = PostForm(request.POST)
            if form.is_valid():

                post.content = form.cleaned_data['content']
                post.save()
                return redirect('view_post', post_id=post_id)

            return render(request,
                          'post/edit_post.html',
                          {'post': post,
                           'error_message': 'Invalid input'})

        form = PostForm(initial={'content': post.content})
        return render(request, 'post/edit_post.html', {'post': post})

    return render(request,
                  'post/post.html',
                  {'post': post,
                   'error_message': 'Really? No you cannot edit this post, this is not your post!'})


def delete_post(request, post_id):
    '''
    Deletes post
    '''
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        return redirect('home')

    return redirect('view_post', post_id=post_id)


def vote_post(request, post_id, vote_type):
    '''
    Votes on post
    '''
    if request.user.is_authenticated:

        post = get_object_or_404(Post, pk=post_id)

        if not PostVote.objects.filter(post=post, user=request.user).exists():
            PostVote.objects.create(
                post=post,
                user=request.user,
                type=vote_type
            )
        else:
            vote = PostVote.objects.get(post=post, user=request.user)
            if vote.type == vote_type:
                vote.delete()
            else:
                vote.type = vote_type
                vote.save()

    return redirect('view_post', post_id=post_id)
