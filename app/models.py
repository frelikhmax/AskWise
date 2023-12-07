# from django.db import models
# from django.contrib.auth.models import User
#
#
# # Create your models here.
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.PROTECT)
#     rating = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"{self.user.__str__()}"
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=25)
#     rating = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"{self.name}"
#
#
# class Question(models.Model):
#     title = models.CharField(max_length=60)
#     content = models.TextField(max_length=1200)
#     author = models.ForeignKey(Profile, on_delete=models.PROTECT)
#     rating = models.IntegerField(default=0)
#     tags = models.ManyToManyField(Tag, related_name='questions')
#
#     def __str__(self):
#         return f"{self.title} {self.content}"
#
#
# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField(max_length=300)
#     author = models.ForeignKey(User, on_delete=models.PROTECT)
#     rating = models.IntegerField(default=0)
#     is_correct = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Answer to '{self.question.__str__()} {self.content}'"


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.db import models
from postgres_copy import CopyManager


# Create your models here.


# class ProfileManager(models.Manager):
#     def best_profiles(self):
#         profiles = self.annotate(
#             # raiting=Coalesce(Sum('user__questions__upvotes__vote')+
#             # Sum('user__answers__upvotes__vote'), 0)
#             raiting=Coalesce(Count('profile__answers'), 0)
#         )
#         return profiles.order_by('-raiting')[:5]
#
#
# class UpvoteManager(models.Manager):
#     use_for_related_fields = True
#
#     def rating(self):
#         rating = self.get_queryset().filter(vote__gt=0).count() - self.get_queryset().filter(vote__lt=0).count()
#         return rating
#
#
# class QuestionManager(models.Manager):
#     def calculate_rating(self):
#         questions = Question.objects.annotate(
#             raiting=Coalesce(Sum('upvotes__vote'), 0)
#         )
#         return questions
#
#     def new(self):
#         questions = self.calculate_rating()
#         return questions.order_by('-date_written', '-raiting')
#
#     def hot(self):
#         questions = self.calculate_rating()
#         return questions.order_by('-raiting')
#
#     def tag(self, tag):
#         questions = self.calculate_rating()
#         questions = questions.filter(tags__name=tag)
#         return questions.order_by('-raiting')
#
#
# class AnswerManager(models.Manager):
#     def calculate_raiting(self):
#         answers = Answer.objects.annotate(
#             raiting=Coalesce(Sum('upvotes__vote'), 0)
#         )
#         return answers
#
#     def hot(self, question_id):
#         answers = self.calculate_raiting()
#         answers = answers.filter(question__id=question_id)
#         return answers.order_by('-raiting')
#
#
# class TagManager(models.Manager):
#     def calculate_questions(self):
#         tags = self.annotate(
#             question_num=Coalesce(Count('question'), 0)
#         )
#         return tags
#
#     def hot(self):
#         tags = self.calculate_questions()
#         return tags.order_by('-question_num')[:10]


class Profile(models.Model):
    registration_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')

    # objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=15)

    # objects = TagManager()

    def __str__(self):
        return self.name


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote')
    )
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # objects = UpvoteManager()


class Question(models.Model):
    title = models.TextField(max_length=60)
    content = models.TextField(max_length=1200)
    profile = models.ForeignKey(Profile, max_length=256, related_name='questions', on_delete=models.PROTECT,
                                default=None)
    publication_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='questions', related_query_name='question')
    upvotes = GenericRelation(Vote)

    # objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    content = models.TextField(max_length=300)
    publication_date = models.DateField(null=True, blank=True)
    profile = models.ForeignKey(Profile, max_length=256, related_name='answers', on_delete=models.PROTECT, default=None)
    question = models.ForeignKey(Question, max_length=256, related_name='answers', on_delete=models.PROTECT)
    upvotes = GenericRelation(Vote)

    # objects = AnswerManager()

    def __str__(self):
        return self.question.title
