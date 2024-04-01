from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages

# Create your views here.
def index(request):
    
    signup_form = forms.CreateUser()
    return render(request, 'login.html',{'signup_form':signup_form})

def DashBoard(request):
    return render(request, 'dashboard.html' ,{'user':request.user})
    
def SignUp(request):
    
    if request.method == 'POST':
        
        form = forms.CreateUser(request.POST)
       
        if form.is_valid():
            try:
                
                print(form.cleaned_data['first_name'] + form.cleaned_data['last_name'])
                user = form.save(commit=False)
                user.username = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
                form.save()
                
                return redirect('index')
            except Exception as e:
                print(e)
        else:
            return render(request, 'login.html',{'signUp_form':form})
    else:
        form = forms.CreateUser()
    return render(request, 'login.html',{'signUp_form':form})

def LoginUsr(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           
            return redirect('dashboard')  
        else:
            
            messages.error(request, 'Invalid username or password.')
   
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')