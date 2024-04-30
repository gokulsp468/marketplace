# serializers.py
from rest_framework import serializers

class StripeCheckoutSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    unit_amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=3, default='usd')
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()
    customer_email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255)  # Field for customer name
    customer_address = serializers.CharField(max_length=255)  # Field for customer address

    def create(self, validated_data):
        # You can handle the Stripe session creation logic here
        # Use the validated data to create the checkout session with Stripe
        # Return the session ID or any relevant data
        return validated_data

