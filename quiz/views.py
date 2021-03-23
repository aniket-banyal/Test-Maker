from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import Quiz, Question, Choice, Answer
from datetime import datetime
import pytz


class QuizDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Quiz

    def test_func(self):
        return self.request.user == self.get_object().maker


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz

    def get_queryset(self):
        return Quiz.objects.filter(maker=self.request.user).order_by('-id')
    # paginate_by = 100


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz-list')

    def test_func(self):
        return self.request.user == self.get_object().maker


def createQuestions(data, quiz, startIdx):
    for i in range(startIdx, len(data)):
        try:
            question = Question.objects.create(
                question=data[f'q_{i}'], quiz=quiz, point=data[f'{i}_point'])

            for j in range(1, len(data)):
                try:
                    Choice.objects.create(
                        choice=data[f'{i}_option{j}'], question=question)
                except KeyError:
                    break

            Answer.objects.create(
                answer=data[f'{i}_radio_option'], question=question)

        except KeyError:
            break


def createQuiz(data, user):
    if 'timer-enabled' in data:
        timeLimit = int(data['time-limit'])

        if data['start-date'] != '' and data['start-time'] != '':
            hour = int(data['start-time'][:2])
            minute = int(data['start-time'][3:])
            startDate = data['start-date']
            # tz = pytz.timezone('Asia/Kolkata')
            startDateTime = datetime.strptime(
                startDate, '%Y-%m-%d').replace(hour=hour, minute=minute)
        else:
            startDateTime = None
    else:
        timeLimit = startDateTime = None

    quiz = Quiz.objects.create(
        name=data['quiz'], maker=user, startDateTime=startDateTime, timeLimit=timeLimit)

    createQuestions(data, quiz, 1)


@login_required
def newQuiz(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)

        createQuiz(data, request.user)

        return redirect('quiz-list')

    defaultNumberOfChoices = range(1, 5)
    return render(request, 'quiz/new_quiz.html', {'defaultNumberOfChoices': defaultNumberOfChoices})


def _updateQuiz(data, quiz):
    quiz.name = data['quiz']

    if 'timer-enabled' in data:
        quiz.timeLimit = int(data['time-limit'])

        if data['start-date'] != '' and data['start-time'] != '':
            hour = int(data['start-time'][:2])
            minute = int(data['start-time'][3:])
            startDate = data['start-date']

            # tz = pytz.timezone('Asia/Kolkata')
            quiz.startDateTime = datetime.strptime(
                startDate, '%Y-%m-%d').replace(hour=hour, minute=minute)
        else:
            quiz.startDateTime = None
    else:
        quiz.timeLimit = quiz.startDateTime = None

    quiz.save()

    i = 1
    more_questions_left = True
    for question in quiz.question_set.all():
        try:
            question.question = data[f'q_{i}']
            question.point = data[f'{i}_point']
            question.save()

            j = 1
            for choice in question.choice_set.all():
                choice.choice = data[f'{i}_option{j}']
                choice.save()
                j += 1

            answer = question.answer
            answer.answer = data[f'{i}_radio_option']
            answer.save()
        except KeyError:
            question.delete()
            more_questions_left = False

        i += 1

    if more_questions_left:
        createQuestions(data, quiz, i)


@login_required
def updateQuiz(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.user != quiz.maker:
        raise PermissionDenied

    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        _updateQuiz(data, quiz)

        return redirect('quiz-list')

    startDateTime = quiz.startDateTime
    if startDateTime is not None:
        startDate = startDateTime.date().strftime('%Y-%m-%d')
        startTime = startDateTime.time().strftime('%H:%M')
    else:
        startDate = startTime = None

    return render(request, 'quiz/quiz_update.html', {'quiz': quiz, 'startDate': startDate, 'startTime': startTime})


@require_POST
def quizDuplicate(request, pk):
    parentQuiz = get_object_or_404(Quiz, id=pk)

    if request.user != parentQuiz.maker:
        raise PermissionDenied

    data = request.POST.dict()
    quiz = Quiz.objects.create(name=data['quiz'], maker=request.user,
                               startDateTime=parentQuiz.startDateTime, timeLimit=parentQuiz.timeLimit)

    for question in parentQuiz.question_set.all():
        duplicate_question = Question.objects.create(
            question=question, quiz=quiz, point=question.point)

        for choice in question.choice_set.all():
            Choice.objects.create(
                choice=choice, question=duplicate_question)

        Answer.objects.create(
            answer=question.answer.answer, question=duplicate_question)

    return redirect('quiz-update', pk=quiz.id)


@login_required
def quizResult(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    print(request.user)
    if request.user != quiz.maker:
        raise PermissionDenied
    takers = quiz.taker_set.all()
    takers_list = list(takers.values())

    i = 0

    total = 0
    for question in quiz.question_set.all():
        total += question.point

    for taker in takers:
        score = 0
        for answer in taker.answer_set.all():
            if answer.quiz == quiz:
                point = answer.real_answer.question.point
                if answer.real_answer.answer == answer.answer:
                    score += point

        takers_list[i]['score'] = f'{score}/{total}'
        i += 1

    return render(request, 'quiz/result.html', {'quiz': quiz, 'takers': takers_list})
