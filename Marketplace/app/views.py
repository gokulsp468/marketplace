from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from . import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

# Create your views here.


def DashBoard(request):
    product_list = None
    sort_by = request.GET.get('sort_by', 'product_title') 
    sort_order = request.GET.get('sort_order', 'asc')  
    add_product_form = forms.AddProduct()
    if request.method == 'POST':
        # Accessing form data sent via POST
        search_query = request.POST.get('search','').strip()  
        if search_query:
           
           product_list = models.Products.objects.filter(
                Q(product_title__icontains=search_query) |
                Q(product_description__icontains=search_query) |
                Q(product_price__icontains=search_query)
            )
        else:
            
            product_list = models.Products.objects.filter(user=request.user).all() 
    
    else:
        product_list = models.Products.objects.filter(user=request.user).all() 
        if sort_order == 'asc':
            product_list = product_list.order_by(sort_by)
        else:
            product_list = product_list.order_by(f'-{sort_by}')
        
    
    return render(request, 'dashboard.html', {'user': request.user, 'add_product_form': add_product_form, 'product_list':product_list})
    
def SignUp(request):
    
    if request.method == 'POST':
        
        form = forms.CustomUserCreationForm(request.POST)
       
        if form.is_valid():
            try:
                username = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                if models.CustomUser.objects.filter(username=username).exists():
                    raise ValidationError("username already exist")
                if models.CustomUser.objects.filter(email=email).exists():
                    raise ValidationError("email already exist")
                print(form.cleaned_data['first_name'] + form.cleaned_data['last_name'])
                user = form.save(commit=False)
                user.username = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
                form.save()
                
                return redirect('signUp')
            except Exception as e:
                messages.error(request, e)
        else:
            return render(request, 'login.html',{'signUp_form':form})
    else:
        form = forms.CustomUserCreationForm()
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
    return redirect('signUp')


def add_products(request):
    if request.method == "POST":
        add_product_form = forms.AddProduct(request.POST, request.FILES)
        
        try:
    
            if add_product_form.is_valid():
                
                add_product = add_product_form.save(commit=False)
                add_product.user = request.user
                add_product.save()
                return redirect('dashboard')
            else:
                raise ValidationError(add_product_form.errors) 
        except Exception as e:
            messages.error(request,e)
    else:
        return redirect('dashboard')
    
    
def edit_product(request ,id):
    if request.method == "POST":
        product = get_object_or_404(models.Products, id=id)
        print(product)
        add_product_form = forms.AddProduct(request.POST, request.FILES, instance=product)
        try:
            
            if add_product_form.is_valid():
                
                add_product_form.save()
                messages.success(request,"successfully edited")
                return redirect('dashboard')
            else:
               raise ValidationError(add_product_form.errors) 
        except Exception as e:
            messages.error(request,e)
    else:
        return redirect('dashboard')
    return redirect('dashboard')

def delete_product(request, id):
    if request.method == "POST":
        product = get_object_or_404(models.Products, id=id)
        product.delete()
        messages.success(request,"deleted successfully")
        
        
    return redirect('dashboard')