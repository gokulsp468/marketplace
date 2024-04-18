import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CardInformationSerializer
from drf_yasg.utils import swagger_auto_schema
import os 




class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer
    @swagger_auto_schema(request_body= CardInformationSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}  # Initialize the response dictionary
        if serializer.is_valid():
            data_dict = serializer.validated_data
            
            # Set the Stripe API key from settings
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            
            # Call the stripe_card_payment method and assign its response to response dictionary
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            # If serializer is not valid, construct error response
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
                
        # Return the constructed response
        return Response(response)

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
                'number': data_dict['card_number'],
                'exp_month': data_dict['expiry_month'],
                'exp_year': data_dict['expiry_year'],
                'cvc': data_dict['cvc'],
            }

            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=10000, 
                currency='inr',
                payment_method_types=['card'],  # Specify accepted payment method types
                confirm=True,  # Automatically confirm the payment intent
                payment_method=card_details  # Pass the card details directly
            )
            
            # Check if payment succeeded
            if payment_intent.status == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "payment_intent": payment_intent
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": payment_intent
                }
        except stripe.error.CardError as e:
            # Handle card errors
            response = {
                'error': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
            }
        except Exception as e:
            # Handle other exceptions
            response = {
                'error': str(e),
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
            }
        return response
