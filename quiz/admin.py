from django.contrib import admin

from .models import Quiz, Question, Choice, McqAnswer, CheckboxAnswer, ShortAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(McqAnswer)
admin.site.register(CheckboxAnswer)
admin.site.register(ShortAnswer)
