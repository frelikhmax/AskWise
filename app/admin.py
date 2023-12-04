from django.contrib import admin


# Register your models here.

from .models import Profile, Tag, Question, Answer

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
