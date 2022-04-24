from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile,Post
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')

# LOGIN VIEW FOR USER
def Login(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect("profile")
    return render(request,'Login.html')

def Logout(request):
    logout(request)
    return redirect("Login")

def create_profile(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        image = request.FILES['image']
        user = User.objects.create_user(username=username,password=password)
        profile = Profile.objects.create(user=user,profile_picture=image)
        if profile:
            messages.success(request,'Profile Created Please Login')
            return redirect("Login")
    return render(request,'Signup.html')

def profile(request,id=None):
    if not request.user.is_authenticated:
        return redirect("Login")
    if id is not None:
        profile_id = Profile.objects.get(id=id)
        posts = Post.objects.filter(profile=profile_id)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
    else:
        profile_id = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(user=request.user)
        posts_num = posts.count()
        profile = Profile.objects.get(user=request.user)
        profileimage = profile.profile_picture.url
    return render(request,'profile.html',{'profile':profile_id,'profileimage':profileimage,'profile_of_user':True,'posts':posts,'posts_num':posts_num})