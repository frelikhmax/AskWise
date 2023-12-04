from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.__str__()}"


class Tag(models.Model):
    name = models.CharField(max_length=25)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(max_length=1200)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):
        return f"{self.title} {self.content}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to '{self.question.__str__()} {self.content}'"
