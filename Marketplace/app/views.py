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
# Create your views here.


# @permission_classes([IsAuthenticated])
# class ProductsView(APIView):
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('sort_by', openapi.IN_QUERY, description="Field to sort by", type=openapi.TYPE_STRING),
#             openapi.Parameter('sort_order', openapi.IN_QUERY, description="Sort order (asc or desc)", type=openapi.TYPE_STRING),
#             openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
#         ]
#     )
#     def get(self, request):
#         if not request.user.is_authenticated :
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
#         if request.user.user_type == 'seller' or request.user.user_type == 'customer':
#             product_list = models.Products.objects.filter(user=request.user).all()
#         elif request.user.user_type == 'admin':
#             product_list = models.Products.objects.all()
            
#         sort_by = request.GET.get('sort_by', 'product_title')
#         sort_order = request.GET.get('sort_order', 'asc')
#         search_query = request.GET.get('search', '').strip()
#         if search_query:
#             product_list = product_list.filter(
#                 Q(product_title__icontains=search_query) |
#                 Q(product_description__icontains=search_query) |
#                 Q(product_price__icontains=search_query)
#             )

#         if sort_order == 'asc':
#             product_list = product_list.order_by(sort_by)
#         else:
#             product_list = product_list.order_by(f'-{sort_by}')

#         serializer = serializers.ProductSerializer(product_list, many=True)
#         return Response(serializer.data)
    
#     @swagger_auto_schema(
#         request_body=serializers.ProductSerializer
#     )
#     def post(self, request):
#         serializer = serializers.ProductSerializer(data = request.data, context = {'request':request})
#         try:
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'data':serializer.data,'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'errors': "failed"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# @permission_classes([IsAuthenticated])   
# class ProductPatch(APIView):
    # @swagger_auto_schema(
    #     request_body=serializers.ProductSerializer,
        
    # )
        
    # def patch(self, request, pk):
    #     product = models.Products.objects.get(pk=pk)
    #     if product.user != request.user:
    #         return Response({'error': 'You do not have permission to edit this product'}, status=status.HTTP_403_FORBIDDEN)
        
    #     serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
    #     try:
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter('id', openapi.IN_PATH, description="ID of the product to delete", type=openapi.TYPE_INTEGER)]
    # )
    # def delete(self, request, pk):
    #     try:
    #         product = models.Products.objects.get(pk=pk)
    #     except models.Products.DoesNotExist:
    #         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    renderer_classes = [CustomJSONRenderer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == 'admin' or user.user_type == 'customer':
                return models.Products.objects.all()
            else:
                return models.Products.objects.filter(user=user)
        else:
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
 



