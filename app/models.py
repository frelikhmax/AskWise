from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.db import models


# Create your models here.


class ProfileManager(models.Manager):
    def best(self):
        profiles = self.annotate(
            # rating=Coalesce(Sum('questions__votes__vote_type')+ Sum('answers__votes__vote_type'), 0)
            rating=Coalesce(Count('answers'), 0)

        )
        # return profiles.order_by('-rating')
        return profiles


class UpvoteManager(models.Manager):
    use_for_related_fields = True

    def rating(self):
        rating = self.get_queryset().filter(vote__gt=0).count() - self.get_queryset().filter(vote__lt=0).count()
        return rating


class QuestionManager(models.Manager):
    def calculate_rating(self):
        questions = Question.objects.annotate(
            rating=Coalesce(Sum('votes__vote_type'), 0)
        )
        return questions

    def new(self):
        return self.order_by('-publication_date')

    def hot(self):
        questions = self.calculate_rating()
        return questions.order_by('-rating')

    def tag(self, tag):
        questions = self.filter(tags__name=tag)
        return questions



class AnswerManager(models.Manager):
    def calculate_rating(self):
        answers = Answer.objects.annotate(
            rating=Coalesce(Sum('votes__vote_type'), 0)
        )
        return answers

    def hot(self, question_id):
        answers = self.filter(question__id=question_id)
        answers = answers.calculate_rating()
        return answers.order_by('-rating')

    def question(self, question):
        answers = self.filter(question=question)
        return answers


class TagManager(models.Manager):
    def calculate_questions(self):
        tags = self.annotate(
            question_num=Coalesce(Count('question'), 0)
        )
        return tags

    def hot(self):
        tags = self.calculate_questions()
        return tags


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote')
    )
    vote_type = models.SmallIntegerField(choices=VOTE_CHOICES)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # objects = UpvoteManager()


class Question(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(max_length=1200)
    profile = models.ForeignKey('Profile', related_name='questions', on_delete=models.PROTECT)
    publication_date = models.DateField()
    tags = models.ManyToManyField('Tag', related_name='questions', related_query_name='question')
    votes = GenericRelation(Vote)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.CharField(max_length=300)
    publication_date = models.DateField(null=True, blank=True)
    profile = models.ForeignKey('Profile', related_name='answers', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.PROTECT)
    votes = GenericRelation(Vote)

    objects = AnswerManager()

    def __str__(self):
        return self.question.title


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=16)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    registration_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username
