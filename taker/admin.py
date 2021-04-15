from django.contrib import admin

from .models import Taker, McqAnswer, CheckboxAnswer, ShortAnswer

admin.site.register(Taker)
admin.site.register(McqAnswer)
admin.site.register(CheckboxAnswer)
admin.site.register(ShortAnswer)
