from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm
from quiz.models import Quiz
from .models import Taker
from taker.utils.helpers import formatDateTimeForJavascript, hasTakerAlreadyTakenQuiz
from taker.utils.email import setSendEmailTimer
from taker.utils.createTakerAnswers import createTakerAnswers
from taker.utils.takerResult import createTakerQuestionsList
from datetime import datetime, timedelta
import pytz


def takeQuizRegister(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            taker = form.save(commit=False)

            if hasTakerAlreadyTakenQuiz(taker, quiz):
                return render(request, 'taker/already_taken_quiz.html')

            taker.save()

            return redirect('take-quiz', pk=pk, taker_id=taker.id)

    else:
        if quiz.isOver():
            return render(request, 'taker/quiz_not_accepting_responses.html')

        form = UserRegisterForm()

    return render(request, 'taker/register.html', {'form': form})


@never_cache
def takeQuiz(request, pk, taker_id):
    quiz = get_object_or_404(Quiz, id=pk)
    taker = get_object_or_404(Taker, id=taker_id)

    if taker.quiz == quiz:
        return render(request, 'taker/already_taken_quiz.html')

    if not quiz.hasStarted():
        return render(request, 'taker/wait_for_quiz_start.html', {'startDateTime': formatDateTimeForJavascript(quiz.startDateTime)})

    if quiz.isOver():
        return render(request, 'taker/quiz_not_accepting_responses.html')

    context = {'quiz': quiz, 'taker_id': taker_id,
               'endDateTime': formatDateTimeForJavascript(quiz.endDateTime)}

    return render(request, 'taker/take_quiz.html', context)


BUFFER_TIME = 5


@ require_POST
def submitQuiz(request, pk, taker_id):
    quiz = get_object_or_404(Quiz, id=pk)
    taker = get_object_or_404(Taker, id=taker_id)

    if taker.quiz == quiz:
        return render(request, 'taker/already_taken_quiz.html')

    now = datetime.now().replace(tzinfo=pytz.UTC)
    endDateTime = quiz.endDateTime

    # print('\nstartDateTime- ', startDateTime)
    # print('endDateTime-   ', endDateTime)
    # print('datetime.now-  ', datetime.now(), '\n')

    # if taker manipulates seconds or minutes in console of take_quiz and submits after endDateTime, then to handle that
    if endDateTime + timedelta(seconds=BUFFER_TIME) < now:
        taker.delete()
        return render(request, 'taker/quiz_not_accepting_responses.html')

    data = request.POST.dict()
    print(data)

    taker.quiz = quiz
    taker.save()

    createTakerAnswers(quiz, taker, data)

    if quiz.isOver():
        return redirect('result', pk=pk, taker_id=taker_id)

    else:
        interval = (endDateTime - now).total_seconds()
        setSendEmailTimer(quiz, taker, interval)

        return render(request, 'taker/quiz_submitted.html', {'taker': taker, 'endDate': endDateTime.date(), 'endTime': endDateTime.time()})


def result(request, pk, taker_id):
    quiz = get_object_or_404(Quiz, id=pk)
    taker = get_object_or_404(Taker, id=taker_id)

    # if this url is visited by a logged in user who has not created this quiz deny
    # but still need to solve that anonymous user can still access this url
    if not request.user.is_anonymous:
        if request.user != quiz.maker:
            raise PermissionDenied

    takerQuestions = createTakerQuestionsList(quiz.question_set.all(), taker)

    score = taker.score

    return render(request, 'taker/result.html', {'score': score, 'quiz': quiz, 'questions': takerQuestions})
