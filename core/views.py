from django.shortcuts import render, redirect
from .forms import BlogPostForm, BlogPost, RegisterForm, UpdateUserForm, UpdateProfileForm, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .serializers import BlogPostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})    

@login_required
def create_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   
            post.save()
            return redirect('post_list')      
    else:
        form = BlogPostForm()

    return render(request, 'core/create_post.html', {'form': form})

def post_list(request):
    posts = BlogPost.objects.all().order_by('-id') 
    return render(request, 'core/post_list.html', {'posts': posts})


@api_view(['GET'])
def api_posts(request):
    posts = BlogPost.objects.all()
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if profile.profile_pic and not profile.profile_pic.name:
        profile.profile_pic = None
        profile.save()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)
        
    return render(request, 'core/profile.html', {'user_form': user_form,'profile_form': profile_form,'profile': profile})