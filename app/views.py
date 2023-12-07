import math

from app.models import Tag, Profile, Question, Answer

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

TAGS = [
    {'name': 'cats', 'color': 'text-bg-primary'},
    {'name': 'algebra', 'color': 'text-bg-secondary'},
    {'name': 'books', 'color': 'text-bg-success'},
    {'name': 'pharm', 'color': 'text-bg-danger'},
    {'name': 'cssports', 'color': 'text-bg-warning'},
    {'name': 'italian', 'color': 'text-bg-info'}
]


def paginate(objects, request, per_page=3):
    paginator = Paginator(objects, per_page)

    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            page = paginator.num_pages
    except ValueError:
        page = 1

    return paginator.page(page), page, paginator.num_pages


# Create your views here.
def index(request):
    params, page, pages_number = paginate(Question.objects.all(), request, 4)
    return render(request, 'index.html',
                  {'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1, 'pages_number': pages_number,
                   'tags': TAGS})


def ask(request):
    return render(request, 'ask.html')


def hot(request):
    params, page, pages_number = paginate(Question.objects.all(), request, 4)
    return render(request, 'hot.html',
                  {'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1, 'pages_number': pages_number,
                   'tags': TAGS})


def login(requset):
    return render(requset, 'login.html')


def question(request, question_id):
    item = Question.objects.all()[question_id - 1]
    params, page, pages_number = paginate(Answer.objects.filter(question=item), request)
    return render(request, 'question.html', {'question': item,
                                             'answers': params, 'page': page, 'prev': page - 1, 'fol': page + 1,
                                             'pages_number': pages_number, 'tags': TAGS})


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    tagg = get_object_or_404(Tag, name=tag_name)
    items = Question.objects.filter(tags__in=[tagg])
    params, page, pages_number = paginate(items, request, 2)

    return render(request, 'tag.html',
                  {'tag': tag_name, 'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1,
                   'pages_number': pages_number, 'tags': TAGS})
