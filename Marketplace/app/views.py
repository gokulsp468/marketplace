from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth import authenticate, login ,logout
from . import models
from django.db.models import Q
from rest_framework.decorators import  permission_classes
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, renderer_classes
from .renderer import CustomJSONRenderer
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)



class ProductsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    renderer_classes = [CustomJSONRenderer]

    def get_queryset(self):
        user = self.request.user
        logger.debug("Fetching queryset for user: %s", user.username)
        if user.is_authenticated:
            if user.user_type == 'admin' or user.user_type == 'customer':
                return models.Products.objects.all()
            else:
                return models.Products.objects.filter(user=user)
        else:
            logger.warning("Unauthenticated access attempted.")
            return models.Products.objects.none()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('sort_by', openapi.IN_QUERY, description="Field to sort by", type=openapi.TYPE_STRING),
            openapi.Parameter('sort_order', openapi.IN_QUERY, description="Sort order (asc or desc)", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        logger.debug("Listing products, total count: %d", queryset.count())
       
        sort_by = request.query_params.get('sort_by', 'product_title')
        sort_order = request.query_params.get('sort_order', 'asc')
        search_query = request.query_params.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(product_title__icontains=search_query) |
                Q(product_description__icontains=search_query) |
                Q(product_price__icontains=search_query)
            )

        if sort_order == 'asc':
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by(f'-{sort_by}')

        serializer = self.get_serializer(queryset, many=True)
        
        # Check if any products were retrieved
        if queryset.exists():
            message = 'Products retrieved successfully'
        else:
            message = 'No products found'
        
        return Response({'data': serializer.data, 'message': message}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'data': serializer.data, 'message': 'Product added successfully'}, status=status.HTTP_201_CREATED, headers=headers)

       
       
 
 
       
@swagger_auto_schema(
    method='post',
    operation_description="Add item(s) to cart",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['product_id', 'quantity'],
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product to add to cart'),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the product to add to cart'),
        },
    )    )   
@swagger_auto_schema(
    method='delete',
    operation_description="Delete Products from cart",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['product_id'],
        properties={
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product to add to cart'),
            
        },
    )    ) 
@api_view(['GET','POST','DELETE'])
@renderer_classes([CustomJSONRenderer])   
def cart_list(request):
    if not request.user.is_authenticated or request.user.user_type != 'customer':
        response_data = {
                'error_message': 'unauthorized'
            }
        return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        try:
            customer_cart = models.Cart.objects.get(user=request.user)
            cart_items = models.CartProduct.objects.filter(cart=customer_cart)
            serializer = serializers.CartItemSerializer(cart_items, many=True)
            
            response_data = {
            'data': serializer.data,
            'total_cash': customer_cart.total_cash(),
            'message': 'successfully retrieved cart'
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except models.Cart.DoesNotExist:
            response_data = {
                'error_message': 'Cart not found'
            }
            return Response(response_data,status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'error_message': 'Product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = models.Products.objects.get(pk=product_id)
        except models.Products.DoesNotExist:
            
            return Response({'error_message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            customer_cart = models.Cart.objects.get(user=request.user)
        except models.Cart.DoesNotExist:
            customer_cart = models.Cart.objects.create(user=request.user)

        try:
            cart_item = models.CartProduct.objects.get(cart=customer_cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()
        except models.CartProduct.DoesNotExist:
            cart_item = models.CartProduct.objects.create(cart=customer_cart, product=product, quantity=int(quantity))

        serializer = serializers.CartItemSerializer(cart_item)
        response_data = {
                'data': serializer.data,
                'message':'Product successfully added to cart'
            }
        return Response(response_data, status=status.HTTP_201_CREATED)
       
       
       
    
    elif request.method == 'DELETE':
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error_message': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = models.Products.objects.get(pk=product_id)
        except models.Products.DoesNotExist:
            return Response({'error_message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            customer_cart = models.Cart.objects.get(user=request.user)
        except models.Cart.DoesNotExist:
            return Response({'error_message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = models.CartProduct.objects.get(cart=customer_cart, product=product)
            cart_item.delete()
            response_data = {
                'message': 'Product deleted from cart'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except models.CartProduct.DoesNotExist:
            return Response({'error_message': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)
 


########################################################################################################################

def chat(request):
    refresh = RefreshToken.for_user(request.user)
    
    if request.user.user_type == 'admin':
        chats = models.Chat.objects.all()
        return render(request, 'adminchatbox.html',{'chats':chats,'token':refresh.access_token})
               
    return render(request, 'socket.html',{'token':refresh.access_token})


def supportChat(request,roomName):
    return render(request, 'supportchat.html',{'roomName':roomName,'sender':request.user})
    
    

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
            if request.user.user_type == 'customer':
                product_list = models.Products.objects.all() 
            else:
                product_list = models.Products.objects.filter(user=request.user).all() 
    
    else:
        print(request.user.user_type)
        if request.user.user_type == 'customer':
            product_list = models.Products.objects.all() 
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