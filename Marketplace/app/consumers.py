import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import CustomUser,ChatMessage ,Chat 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class ChatConsumer(WebsocketConsumer):
    def connect(self):
    
        token = None
        room_param = None
        sender = None

        query_params = self.scope['query_string'].decode().split('&')
        for param in query_params:
            key, value = param.split('=')
            if key == 'token':
                token = value
            elif key == 'room':
                room_param = value
            elif key == 'sender':
                sender = value

        # print("Token:", token)
        # print("Room:", room_param)
        # print("Sender:", sender)

        if token:
            
            user =  self.get_user(token)
        else:
            user =CustomUser.objects.get(username=room_param)
            
            
            
        
        if sender:
            self.sender = CustomUser.objects.get(username=sender)
        else:
            self.sender  = CustomUser.objects.get(username=user.username)
            
            
            
        if user is not None:
            
            self.user = user
            if room_param:
                
                self.room_group_name = f"user_{room_param}"
            else:
                
                self.room_group_name = f"user_{user.username}"
                
            print(self.room_group_name)
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            
            self.accept()
            self.send_previous_messages()
        else:
            
            self.close()

    def get_user(self, token):
        try:
            # Decode the access token
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            # Retrieve the user object from the database
            user =CustomUser.objects.get(id=user_id)
            return user
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None
        
        
    def send_previous_messages(self):
        
        chat = Chat.objects.filter(user=self.user).first()

        if chat:
            # Retrieve all messages associated with the chat object
            previous_messages = ChatMessage.objects.filter(chat=chat)

            # Send each message to the client
            for message in previous_messages:
                self.send(text_data=json.dumps({
                    'type': 'chat',
                    'sender':message.sender.get_username(),
                    'message': message.text
                }))


   
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the chat message to the database
        self.save_chat_message(message)

        # Broadcast the message to the user's room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender':self.sender,
                'message': message
            }
        )

    
    def save_chat_message(self, message):
        # Save the chat message to the database
        chat, created = Chat.objects.get_or_create(user=self.user)

        # Create a new message object and save it
        ChatMessage.objects.create(
            chat=chat,
            sender=self.sender,
            text=message
        )
        
        
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        # Send the message back to the client
        self.send(text_data=json.dumps({
            'type': 'chat',
            'sender':sender.get_username(),
            'message': message
        }))

    def disconnect(self, close_code):
        # Remove the user from their room group when they disconnect
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
