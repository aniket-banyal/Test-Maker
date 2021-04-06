from datetime import datetime
from taker.models import Taker


def hasTakerAlreadyTakenQuiz(user, quiz):
    if Taker.objects.filter(email=user.email).exists():
        for existing_taker in Taker.objects.filter(email=user.email):
            if existing_taker.quiz == quiz:
                return True
    return False


def formatDateTimeForJavascript(d):
    return datetime.strftime(d, '%d-%b-%Y %H:%M:%S')
