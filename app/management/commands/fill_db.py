from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random
from app.models import Profile, Tag, Vote, Question, Answer

fake = Faker()


# class Command(BaseCommand):
#     help = 'Fill the database with test data'
#
#     def add_arguments(self, parser):
#         parser.add_argument('ratio', type=int, help='Coefficient for data generation')
#
#     def handle(self, *args, **kwargs):
#         ratio = kwargs['ratio']
#         self.create_users(ratio)
#         self.create_tags(ratio)
#         self.create_questions(ratio)
#         self.create_answers(ratio)
#         self.create_votes(ratio)
#
#     def create_users(self, ratio):
#         for _ in range(ratio):
#             username = fake.user_name()
#             email = fake.email()
#             password = fake.password()
#             User.objects.create_user(username=username, email=email, password=password)
#
#     def create_tags(self, ratio):
#         for _ in range(ratio):
#             Tag.objects.create(name=fake.word())
#
#     def create_questions(self, ratio):
#         for _ in range(ratio * 10):
#             title = fake.sentence()
#             content = fake.paragraph()
#             user = random.choice(Profile.objects.all())
#             publication_date = fake.date_between(start_date='-30d', end_date='today')
#             question = Question.objects.create(title=title, content=content, user=user,
#                                                publication_date=publication_date)
#             question.tags.set(random.sample(Tag.objects.all(), k=random.randint(1, ratio)))
#
#     def create_answers(self, ratio):
#         for question in Question.objects.all():
#             for _ in range(ratio * 10):
#                 content = fake.paragraph()
#                 user = random.choice(Profile.objects.all())
#                 publication_date = fake.date_between(start_date=question.publication_date, end_date='today')
#                 Answer.objects.create(content=content, user=user, question=question, publication_date=publication_date)
#
#     def create_votes(self, ratio):
#         for _ in range(ratio * 200):
#             vote = random.choice([-1, 1])
#             user = random.choice(Profile.objects.all())
#             content_type = random.choice(["question", "answer"])
#             if content_type == "question":
#                 object_id = random.choice(Question.objects.all()).id
#             else:
#                 object_id = random.choice(Answer.objects.all()).id
#             Vote.objects.create(vote=vote, user=user, content_type=content_type, object_id=object_id)


# def fake_thing():
#     return dict(
#         char=fake.name(),
#         text=fake.text(),
#         integer=fake.pyint(),
#         float=fake.pyfloat(),
#         boolean=fake.pybool(),
#     )
#
#
# n_things = 100
# things = [fake_thing() for _ in range(n_things)]
#
#
# def fake_user():
#     username = fake.user_name()
#     email = fake.email()
#     password = fake.password()
#     User.objects.create_user(username=username, email=email, password=password)
#     return email
#
#
# def fake_profile():
#     registration_date = fake.date_between(start_date='-1y', end_date='today')
#     birth_date = fake.date_between(start_date='-45y', end_date='-8y')
#
#     user = User.objects.filter(email=fake_user())
#
#
# def fake_tag():
#     name = fake.word()
#
#
# def fake_vote():
#     vote = random.choice([-1, 1])
#     profile = random.choice(Profile.objects.all())
#     content_type = random.choice(["question", "answer"])
#     if content_type == "question":
#         object_id = random.choice(Question.objects.all()).id
#     else:
#         object_id = random.choice(Answer.objects.all()).id
#     Vote.objects.create(vote=vote, profile=profile, content_type=content_type, object_id=object_id)
#
#
# def fake_question():
#     title = fake.sentence()
#     content = fake.paragraph()
#     profile = random.choice(Profile.objects.all())
#     publication_date = fake.date_between(start_date=profile.registration_date, end_date='today')
#     question = Question.objects.create(title=title, content=content, profile=profile, publication_date=publication_date)
#     question.tags.set(random.sample(Tag.objects.all(), k=(random.randint(1, 10))))
#
#
# def fake_answers():
#     content = fake.paragraph()
#     profile = random.choice(Profile.objects.all())
#     question = random.choice(Question.objects.all())
#     publication_date = fake.date_between(start_date=question.publication_date, end_date='today')
#     answer = Answer.objects.create(content=content, profile=profile, question=question,
#                                    publication_date=publication_date)


#####################3
def fake_user():
    return dict(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password()
    )


def fake_profile():
    return dict(
        registration_date=fake.date_between(start_date='-1y', end_date='today'),
        birth_date=fake.date_between(start_date='-45y', end_date='-8y'),
        user=fake_user()
    )


def fake_tag():
    return dict(
        name=fake.word(),
    )


def fake_vote():
    content_type = random.choice(["question", "answer"])
    return dict(
        vote=random.choice([-1, 1]),
        profile=random.choice(Profile.objects.all()),
        content_type=content_type,
        object_id=(random.choice(Question.objects.all()).id if content_type == "question" else random.choice(
            Answer.objects.all()).id)
    )


def fake_question():
    profile = random.choice(Profile.objects.all())
    return dict(
        title=fake.sentence(),
        content=fake.paragraph(),
        profile=profile,
        publication_date=fake.date_between(start_date=profile.registration_date, end_date='today'),
        tags=random.sample(Tag.objects.all(), k=(random.randint(1, 10)))
    )


def fake_answers():
    question = random.choice(Question.objects.all())
    return dict(
        content=fake.paragraph(),
        profile=random.choice(Profile.objects.all()),
        question=question,
        publication_date=fake.date_between(start_date=question.publication_date, end_date='today')
    )


# profiles = [fake_profile() for _ in range(5)]
#
# for profile in profiles:
#     t = Profile(**profile)
#     t.save()


class Command(BaseCommand):
    help = 'Fill the database with random data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of data to generate')

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.fake_profiles(ratio)
        self.fake_tags(ratio)
        self.fake_votes(ratio)
        self.fake_questions(ratio)
        self.fake_answers(ratio)

    def fake_profiles(self, ratio):
        for _ in range(ratio):
            profile = Profile(registration_date=fake.date_between(start_date='-1y', end_date='today'),
                              birth_date=fake.date_between(start_date='-45y', end_date='-8y'),
                              user=User.objects.create_user(username=fake.user_name(),
                                                            email=fake.email(),
                                                            password=fake.password()))
            profile.save()

    def fake_tags(self, ratio):
        for _ in range(ratio):
            tag = Tag(name=fake.word())
            tag.save()

    def fake_votes(self, ratio):
        for _ in range(ratio):
            content_type_model = random.choice([Question, Answer])
            content_type = ContentType.objects.get_for_model(content_type_model)

            vote = Vote(
                vote=random.choice([-1, 1]),
                profile=random.choice(Profile.objects.all()),
                content_type=content_type,
                object_id=(
                    random.choice(Question.objects.all()).id if content_type_model == Question else random.choice(
                        Answer.objects.all()).id
                )
            )
            vote.save()

    def fake_questions(self, ratio):
        for _ in range(ratio):
            profile = random.choice(Profile.objects.all())
            tags = random.sample(list(Tag.objects.all()), k=(random.randint(1, 5)))
            question = Question(
                title=fake.sentence(),
                content=fake.paragraph(),
                profile=profile,
                publication_date=fake.date_between(start_date=profile.registration_date, end_date='today'),
            )
            question.save()
            question.tags.set(tags)  # Используйте метод set() для установки связей "многие ко многим"

    def fake_answers(self, ratio):
        for _ in range(ratio):
            question = random.choice(Question.objects.all())
            answer = Answer(content=fake.paragraph(),
                            profile=random.choice(Profile.objects.all()),
                            question=question,
                            publication_date=fake.date_between(start_date=question.publication_date, end_date='today'))
            answer.save()

    # def populate_users(self, ratio):
    #     User.objects.bulk_create([
    #         User(username=fake.user_name(), email=fake.email(), password=fake.password()) for _ in range(ratio)
    #     ])
    #
    # def populate_tags(self, ratio):
    #     Tag.objects.bulk_create([
    #         Tag(content=fake.word(), rating=random.randint(0, 100)) for _ in range(ratio)
    #     ])
    #
    # def populate_questions(self, ratio):
    #     users = User.objects.all()
    #     tags = Tag.objects.all()
    #
    #     Question.objects.bulk_create([
    #         Question(
    #             title=fake.sentence(),
    #             content=fake.paragraph(),
    #             author=random.choice(users),
    #             rating=random.randint(0, 100),
    #         ) for _ in range(ratio * 10)
    #     ])
    #
    # def populate_answers(self, ratio):
    #     users = User.objects.all()
    #     questions = Question.objects.all()
    #
    #     Answer.objects.bulk_create([
    #         Answer(
    #             question=random.choice(questions),
    #             content=fake.paragraph(),
    #             author=random.choice(users),
    #             is_correct=random.choice([True, False]),
    #             rating=random.randint(0, 100),
    #         ) for _ in range(ratio * 100)
    #     ])
    #
    # def populate_profiles(self, ratio):
    #     users = User.objects.all()
    #
    #     Profile.objects.bulk_create([
    #         Profile(user=user, rating=random.randint(0, 100)) for user in users
    #     ])
