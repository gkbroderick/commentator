from django.db import models

# Create your models here.

class Comment(models.Model):
    comment_text = models.CharField(max_length=1000)
    date_created = models.DateTimeField('date created')
    date_last_edited = models.DateTimeField('last edited')
