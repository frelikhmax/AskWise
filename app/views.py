from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app.forms import LoginForm, RegisterForm, AskForm, AnswerForm
from app.models import Tag, Profile, Question, Answer

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


def paginate(objects, request, per_page=5):
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
    params, page, pages_number = paginate(Question.objects.new(), request, 4)
    return render(request, 'index.html',
                  {'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1, 'pages_number': pages_number,
                   'popular_tags': Tag.objects.hot()[:6], 'best_members': Profile.objects.best()[:4],
                   'is_authenticated': request.user.is_authenticated, 'username': request.user.username})


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        ask_form = AskForm()
    if request.method == 'POST':
        ask_form = AskForm(request.POST, request=request)
        if ask_form.is_valid():
            item = ask_form.save()
            if item:
                return redirect(reverse('question', args=[item.id]))
            else:
                ask_form.add_error(field=None, error="Question saving error")
    return render(request, 'ask.html', {'form': ask_form, 'popular_tags': Tag.objects.hot()[:6],
                                        'best_members': Profile.objects.best()[:4],
                                        'is_authenticated': request.user.is_authenticated,
                                        'username': request.user.username})


def hot(request):
    params, page, pages_number = paginate(Question.objects.hot(), request, 4)
    return render(request, 'hot.html',
                  {'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1, 'pages_number': pages_number,
                   'popular_tags': Tag.objects.hot()[:6], 'best_members': Profile.objects.best()[:4],
                   'is_authenticated': request.user.is_authenticated, 'username': request.user.username})


@csrf_protect
def log_in(request):
    if request.user.is_authenticated:
        log_out(request)
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong username or password")
    return render(request, 'log_in.html', context={'form': login_form, 'popular_tags': Tag.objects.hot()[:6],
                                                   'best_members': Profile.objects.best()[:4],
                                                   'is_authenticated': request.user.is_authenticated,
                                                   'username': request.user.username})


@login_required(login_url='login', redirect_field_name='continue')
def log_out(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def question(request, question_id):
    item = get_object_or_404(Question, id=question_id)
    if request.method == 'GET':
        answer_form = AnswerForm(question=item)
    if request.method == 'POST':

        answer_form = AnswerForm(request=request, question=item, data=request.POST)
        if answer_form.is_valid():
            answer = answer_form.save()

        if answer:

            params, page, pages_number = paginate(Answer.objects.question(item), request, 5)

            page_number = pages_number
            for index, item in enumerate(params.object_list):
                if item == answer:
                    page_number = page if index < 5 else page + index // 5
                    break
            url = f"{reverse('question', args=[question_id])}?page={page_number}#{answer.id}"
            return redirect(url)

        else:
            answer_form.add_error(field=None, error="Answer saving error")

    params, page, pages_number = paginate(Answer.objects.question(item), request, 5)

    return render(request, 'question.html',
                  {'question': item, 'answers': params, 'page': page, 'prev': page - 1, 'fol': page + 1,
                   'pages_number': pages_number, 'form': answer_form, 'popular_tags': Tag.objects.hot()[:6],
                   'best_members': Profile.objects.best()[:4],
                   'is_authenticated': request.user.is_authenticated,
                   'username': request.user.username})


@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    return render(request, 'settings.html',
                  {'popular_tags': Tag.objects.hot()[:6], 'best_members': Profile.objects.best()[:4],
                   'is_authenticated': request.user.is_authenticated, 'username': request.user.username})


def signup(request):
    if request.user.is_authenticated:
        log_out(request)

    if request.method == 'GET':
        profile_form = RegisterForm()
    if request.method == 'POST':
        profile_form = RegisterForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save()
            if profile:
                login(request, profile.user)
                return redirect(reverse('index'))
            else:
                profile_form.add_error(field=None, error="Profile saving error")
    return render(request, 'signup.html', context={'form': profile_form, 'popular_tags': Tag.objects.hot()[:6],
                                                   'best_members': Profile.objects.best()[:4],
                                                   'is_authenticated': request.user.is_authenticated,
                                                   'username': request.user.username})


def tag(request, tag_name):
    params, page, pages_number = paginate(Question.objects.tag(tag_name), request, 4)
    return render(request, 'tag.html',
                  {'tag_name': tag_name, 'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1,
                   'pages_number': pages_number, 'popular_tags': Tag.objects.hot()[:6],
                   'best_members': Profile.objects.best()[:4], 'is_authenticated': request.user.is_authenticated,
                   'username': request.user.username})
