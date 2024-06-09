from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import User
from .models import UserProfile, Post, Follow, Notification
from .forms import PostForm


#@login_required
#def user_list(request):
#    users = User.objects.exclude(id=request.user.id)
#    user_profile = UserProfile.objects.get(user=request.user)
#    following = user_profile.following.values_list('followed_id', flat=True)
#    return render(request, 'social/user_list.html', {'users': users, 'following': following})

@login_required
def user_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    following_ids = user_profile.following.values_list('followed_id', flat=True)
    users_to_follow = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id)
    return render(request, 'social/user_list.html', {'users': users_to_follow, 'following_ids': list(following_ids)})



@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user_profile_to_follow = UserProfile.objects.get(user=user_to_follow)
    user_profile = UserProfile.objects.get(user=request.user)
    Follow.objects.get_or_create(follower=user_profile, followed=user_profile_to_follow)
    Notification.objects.create(user=user_profile_to_follow, text=f"{request.user.username} a commencé à te suivre.")
    return redirect('user_list_to_follow')


@login_required
def home(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    following_ids = user_profile.following.values_list('followed_id', flat=True)
    #posts = Post.objects.filter(author__in=following_ids).order_by('-created_at')
    #posts = Post.objects.filter(author_id__in=following_ids).order_by('-created_at')
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user_profile
            post.save()
            return redirect('home')

    return render(request, 'social/home.html', {'posts': posts, 'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'social/post_detail.html', {'post': post})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.userprofile
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'social/new_post.html', {'form': form})


@login_required
def notifications(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    notifications = Notification.objects.filter(user=user_profile).order_by('-created_at')
    return render(request, 'social/notifications.html', {'notifications': notifications})
