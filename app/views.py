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

QUESTIONS = [
    {
        'id': i,
        'rating_counter': f'{(i * 3 + 1) % 10}',
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}',
        'tags': [TAGS[i % 6]['name'], TAGS[(i + 2) % 6]['name']]
    } for i in range(20)
]

ANSWERS = [
    {
        'id': i,
        'rating_counter': f'{(i * 3 + 1) % 10}',
        'content': f'Content of {i} answer'
    } for i in range(15)
]


def search_questions_for_tag(objects, tag_name):
    items = []
    for question in QUESTIONS:
        for tag in question['tags']:
            if tag == tag_name:
                items.append(question)
    return items


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

    prev = page - 1
    fol = page + 1

    return paginator.page(page), page, prev, fol, paginator.num_pages


# Create your views here.
def index(request):
    params, page, prev, fol, pages_number = paginate(Question.objects.all(), request, 4)
    return render(request, 'index.html',
                  {'questions': params, 'page': page, 'prev': prev, 'fol': fol, 'pages_number': pages_number,
                   'tags': TAGS})


def ask(request):
    return render(request, 'ask.html')


def hot(request):
    params, page, prev, fol, pages_number = paginate(Question.objects.all(), request, 4)
    return render(request, 'hot.html',
                  {'questions': params, 'page': page, 'prev': prev, 'fol': fol, 'pages_number': pages_number,
                   'tags': TAGS})


def login(requset):
    return render(requset, 'login.html')


def question(request, question_id):
    item = Question.objects.all()[question_id - 1]
    params, page, prev, fol, pages_number = paginate(Answer.objects.filter(question=item), request)
    return render(request, 'question.html', {'question': item,
                                             'answers': params, 'page': page, 'prev': prev, 'fol': fol,
                                             'pages_number': pages_number, 'tags': TAGS})


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    tagg = get_object_or_404(Tag, name=tag_name)
    items = Question.objects.filter(tags__in=[tagg])
    params, page, prev, fol, pages_number = paginate(items, request, 2)

    return render(request, 'tag.html', {'tag': tag_name, 'questions': params, 'page': page, 'prev': prev, 'fol': fol,
                                        'pages_number': pages_number, 'tags': TAGS})
