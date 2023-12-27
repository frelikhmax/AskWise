from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ImageField
from django.utils import timezone

from app.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password and password_check and password != password_check:
            raise ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Use set_password to hash the password
        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user,
            birth_date=self.cleaned_data['birth_date'],
            registration_date=timezone.now()
        )

        return profile


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=150, required=True, widget=forms.Textarea(attrs={'rows': 2}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Retrieve and store the request object
        super(AskForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def clean_tags(self):
        raw_tags = self.cleaned_data.get('tags')
        if isinstance(raw_tags, str):
            return [tag.strip() for tag in raw_tags.split()]
        elif isinstance(raw_tags, list):
            return [tag.strip() for tag in raw_tags]
        return []

    def save(self, commit=True):
        question = super().save(commit=False)
        question.profile = Profile.objects.get(user=self.request.user)
        question.publication_date = timezone.now()
        tags = self.clean_tags()
        tag_objects = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
        if commit:
            question.save()

        question.tags.set(tag_objects)
        return question


class AnswerForm(forms.ModelForm):
    content = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={'rows': 5}))

    def __init__(self, question, *args, **kwargs):
        self.question = question
        self.request = kwargs.pop('request', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['content']

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.profile = Profile.objects.get(user=self.request.user)
        answer.question = self.question
        answer.publication_date = timezone.now()
        if commit:
            answer.save()
        return answer


class SettingsForm(forms.ModelForm):
    avatar = ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name:
            self.add_error('first_name', 'First name cannot be empty.')

        if not last_name:
            self.add_error('last_name', 'Last name cannot be empty.')

    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')

        if received_avatar:
            profile.avatar = received_avatar
            profile.save()

        return user

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = self.cleaned_data['password']
    #     password_check = self.cleaned_data['password_check']
    #
    #     if password and password_check and password != password_check:
    #         raise ValidationError("Passwords don't match")
    #
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])  # Use set_password to hash the password
    #     if commit:
    #         user.save()
    #
    #     profile = Profile.objects.create(
    #         user=user,
    #         birth_date=self.cleaned_data['birth_date'],
    #         registration_date=timezone.now()
    #     )
    #
    #     return profile
