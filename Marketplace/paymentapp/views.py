# views.py
import stripe
from django.http import HttpResponse

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StripeCheckoutSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY

@swagger_auto_schema(method='post', request_body=StripeCheckoutSerializer)
@api_view(['POST'])
def create_checkout_session(request):
    serializer = StripeCheckoutSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Create customer with required name and address information
            customer_email = serializer.validated_data.get('customer_email')
            customer_name = serializer.validated_data.get('customer_name')
            customer_address = serializer.validated_data.get('customer_address')

            customer = stripe.Customer.create(
                email=customer_email,
                name=customer_name ,
                address={
                    'city':'dfdfssf',
                    'country':'us',
                    'line1':"fdfsfsf",
                    'postal_code':695126,
                    'state':"kerela",
                    'line2':'fdsfsdfdsf'

                }
            )
            
            # Fetch the customer object again to ensure we have the latest version
        
            

            # Create checkout session using the customer ID
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer=customer.id,
                line_items=[{
                    'price_data': {
                        'currency': serializer.validated_data.get('currency', 'usd'),
                        'product_data': {
                            'name': serializer.validated_data['product_name'],
                        },
                        'unit_amount': serializer.validated_data['unit_amount'],
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=serializer.validated_data['success_url'],
                cancel_url=serializer.validated_data['cancel_url'],
                metadata={
                    'customer_name': customer_name,
                    'customer_address': customer_address,
                },
            )
            return Response({'session_id': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
    
