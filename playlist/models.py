from datetime import timedelta

from django.db import models
from django.utils import timezone

class PlayInstance(models.Model):
    name = models.CharField(max_length=250)
    kexp_play_id = models.PositiveIntegerField()
    airdate = models.DateTimeField('airdate', default=timezone.now)

    def __str__(self):
        return "%s: %s" % (self.name, self.airdate.strftime('%Y-%m-%d %H:%M:%S'))

class Comment(models.Model):
    play_instance = models.ForeignKey(PlayInstance, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    date_created = models.DateTimeField('date created',  default=timezone.now)
    date_last_edited = models.DateTimeField('last edited',  default=timezone.now)

    def __str__(self):
        return "%s, comment on %s" % (self.play_instance, self.date_created.strftime('%Y-%m-%d %H:%M:%S'))
