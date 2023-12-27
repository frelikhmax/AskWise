from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from app.forms import LoginForm, RegisterForm, AskForm, AnswerForm, SettingsForm
from app.models import Tag, Profile, Question, Answer, Vote

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
    questions, page, pages_number = paginate(Question.objects.new(), request, 4)

    return render(request, 'index.html',
                  {'questions': questions, 'page': page, 'prev': page - 1, 'fol': page + 1,
                   'pages_number': pages_number,
                   'popular_tags': Tag.objects.hot()[:6], 'best_members': Profile.objects.best()[:4]})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
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
                                        'best_members': Profile.objects.best()[:4]})


def hot(request):
    params, page, pages_number = paginate(Question.objects.hot(), request, 4)
    return render(request, 'hot.html',
                  {'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1, 'pages_number': pages_number,
                   'popular_tags': Tag.objects.hot()[:6], 'best_members': Profile.objects.best()[:4]})


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
                                                   'best_members': Profile.objects.best()[:4]})


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

    answers = Answer.objects.calculate_ratings_for_question(item)

    answers, page, pages_number = paginate(answers, request, 5)

    question_with_rating = Question.objects.calculate_ratings_for_specific(question_id).first()

    return render(request, 'question.html',
                  {'question': question_with_rating, 'answers': answers, 'page': page, 'prev': page - 1,
                   'fol': page + 1,
                   'pages_number': pages_number, 'form': answer_form, 'popular_tags': Tag.objects.hot()[:6],
                   'best_members': Profile.objects.best()[:4]})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial=model_to_dict(request.user))

    elif request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    else:
        form = SettingsForm()
    return render(request, 'settings.html', context={'form': form, 'popular_tags': Tag.objects.hot()[:6],
                                                     'best_members': Profile.objects.best()[:4]})


@csrf_protect
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
                                                   'best_members': Profile.objects.best()[:4]})


def tag(request, tag_name):
    params, page, pages_number = paginate(Question.objects.tag(tag_name), request, 4)
    return render(request, 'tag.html',
                  {'tag_name': tag_name, 'questions': params, 'page': page, 'prev': page - 1, 'fol': page + 1,
                   'pages_number': pages_number, 'popular_tags': Tag.objects.hot()[:6],
                   'best_members': Profile.objects.best()[:4]})


@login_required(login_url='login', redirect_field_name='continue')
@csrf_protect
def like_question(request):
    id = request.POST.get('question_id')

    question_with_rating = Question.objects.calculate_ratings_for_specific(id).first()
    profile = request.user.profile

    existing_vote = Vote.objects.filter(
        profile=profile,
        content_type=ContentType.objects.get_for_model(Question),
        object_id=id
    ).first()

    if existing_vote:

        if existing_vote.vote_type == 1:
            return JsonResponse({'message': 'Vote already exists', 'count': question_with_rating.rating})
        else:
            existing_vote.delete()

    vote = Vote(
        vote_type=1,
        profile=request.user.profile,
        content_type=ContentType.objects.get_for_model(Question),
        object_id=id
    )
    vote.save()

    question_with_rating.rating += 1

    count = question_with_rating.rating

    return JsonResponse({'count': count})
