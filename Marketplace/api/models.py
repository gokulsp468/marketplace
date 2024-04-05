from django.db import models

class Message(models.Model):
    name = models.TextField(max_length=20)
    age = models.IntegerField()
    


class ApiLog(models.Model):
    api_endpoint = models.TextField(max_length=500)
    response_data = models.TextField(max_length=500)
    request_data = models.TextField(max_length=500)
    status = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.api_endpoint
    