import string
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError
from faker import Faker
import random
from app.models import Profile, Tag, Vote, Question, Answer
from io import StringIO
from contextlib import closing

fake = Faker()


class Command(BaseCommand):
    help = 'Fill the database with random data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']
        # self.fake_profiles(ratio + 1)
        # self.fake_tags(ratio + 1)
        # self.fake_questions(ratio * 10 + 1)
        # self.fake_answers(ratio * 100 + 1)
        # self.fake_votes()
        self.make_vote()

    def make_vote(self):
        profile=Profile.objects.get(pk=10017)
        answer = Answer.objects.get(pk=2000048)
        content_type = ContentType.objects.get_for_model(Answer)
        vote = Vote(
            vote_type=random.choice([-1, 1]),
            profile=profile,
            content_type=content_type,
            object_id=answer.id
        )
        vote.save()


    def fake_profiles(self, ratio):
        profile_objects = []
        for _ in range(ratio):
            while True:
                username = fake.user_name()
                if not User.objects.filter(username=username).exists():
                    break
            profile = dict(registration_date=fake.date_between(start_date='-1y', end_date='today'),
                           birth_date=fake.date_between(start_date='-45y', end_date='-8y'),
                           user=User.objects.create_user(username=username,
                                                         email=fake.email(),
                                                         password=fake.password()))
            t = Profile(**profile)
            profile_objects.append(t)
        Profile.objects.bulk_create(profile_objects)

    def fake_tags(self, ratio):
        for _ in range(ratio):
            while True:
                name = ''
                for _ in range(random.randint(1, 16)):
                    name += random.choice(string.ascii_letters)
                if not Tag.objects.filter(name=name).exists():
                    break

            tag = Tag(name=name)
            tag.save()

    def fake_questions(self, ratio):
        profiles = Profile.objects.all()
        question_objects = []
        for _ in range(ratio):
            profile = random.choice(profiles)
            question = dict(
                title=fake.sentence()[:60].rsplit(' ', 1)[0],
                content=fake.paragraph()[:1200].rsplit(' ', 1)[0],
                profile=profile,
                publication_date=fake.date_between(start_date=profile.registration_date, end_date='today'),
            )
            t = Question(**question)
            question_objects.append(t)
        Question.objects.bulk_create(question_objects)

        tags = Tag.objects.all()
        for question in Question.objects.all():
            question.tags.set(random.sample(list(tags), k=(
                random.randint(1, 10))))

    def fake_answers(self, ratio):
        questions = Question.objects.all()
        profiles = Profile.objects.all()
        for i in range(ratio):
            question = random.choice(questions)
            answer = Answer(content=fake.paragraph()[:300].rsplit(' ', 1)[0],
                            profile=random.choice(profiles),
                            question=question,
                            publication_date=fake.date_between(start_date=question.publication_date, end_date='today'))
            answer.save()

    def fake_votes(self):
        questions = Question.objects.all()
        answers = Answer.objects.all()
        profiles = Profile.objects.all()
        for profile in profiles:
            questions = random.sample(list(questions), 18)
            content_type = ContentType.objects.get_for_model(Question)
            for i in range(18):
                vote = Vote(
                    vote_type=random.choice([-1, 1]),
                    profile=profile,
                    content_type=content_type,
                    object_id=questions[i].id
                )
                vote.save()

            answers = random.sample(list(answers), 182)
            content_type = ContentType.objects.get_for_model(Answer)
            for i in range(182):
                vote = Vote(
                    vote_type=random.choice([-1, 1]),
                    profile=profile,
                    content_type=content_type,
                    object_id=answers[i].id
                )
                vote.save()

