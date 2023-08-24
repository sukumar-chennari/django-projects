from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

@login_required(login_url="/login_page/")
def recipes(request):

    if request.method == 'POST':
        data=request.POST
        r_image=request.FILES.get('r_image')
        r_name=data.get('r_name')
        r_description=data.get('r_description')

        Recipe.objects.create(
            r_name=r_name,
            r_description=r_description,
            r_image=r_image
        )
        return redirect('/recipes/')
    queryset=Recipe.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(r_name__icontains=request.GET.get('search'))
       
    return render(request,'recipes.html',context={'recipes':queryset})

@login_required(login_url="/login_page/")
def update(request,id):
    queryset=Recipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        r_name=data.get('r_name')
        r_description=data.get('r_description')
        r_image=request.FILES.get('r_image')

        queryset.r_name=r_name
        queryset.r_description=r_description

        if r_image:
            queryset.r_image=r_image
        queryset.save()
        return redirect('/recipes/')
    return render(request,'update_recipes.html',context={'recipes':queryset})

@login_required(login_url="/login_page/")
def delete(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def login_page(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username)
        
        if (not  user):
            messages.error(request,'Username invalid')
            return redirect('/login_page/')
        
        user=authenticate(username=username,password=password)

        if user is None:
            messages.error(request,"Enter valid Password")
            return redirect('/login_page/')
        
        else:
            messages.info(request,"Log in succesful")
            login(request,user)
            return redirect('/recipes/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login_page')

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "User Name already taken!!!!!!!")
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)#hashing
        user.save()
        messages.info(request, "Account Created successfully")

    return render(request,'register.html')
