from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=100, blank=False, default=None, unique=True)
    asked_at = models.DateTimeField(default=timezone.now)
    asked_by = CurrentUserField()

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('answers', kwargs={'pk': self.pk})


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    answering_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    answered_by = CurrentUserField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('answers', kwargs={'pk': self.pk})
    
    class Meta:
        get_latest_by = ['answering_time']


