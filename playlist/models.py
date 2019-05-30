from django.db import models
from django.utils import timezone

class PlayInstance(models.Model):
    name = models.CharField(max_length=250)
    kexp_play_id = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    play_instance = models.ForeignKey(PlayInstance, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    date_created = models.DateTimeField('date created',  default=timezone.now)
    date_last_edited = models.DateTimeField('last edited',  default=timezone.now)

    def __str__(self):
        return "%s, %s" % (self.play_instance, date_created)
