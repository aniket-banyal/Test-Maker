from django import template

register = template.Library()


def formatTime(value):
    return f'{value}:00'


register.filter('formatTime', formatTime)
