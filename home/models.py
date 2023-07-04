from django.db import models

# Create your models here.

'''Table to store the JSON data of the Coder of the Month'''
class CoderOfTheMonthJSON(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    json = models.TextField()
    
    def __str__(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")
    
