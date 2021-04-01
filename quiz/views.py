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
from .models import Quiz, Question, Choice, McqAnswer, CheckboxAnswer
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

            createAnswers(data, i, question)

        except KeyError:
            break


def createAnswers(data, q_number, question):
    try:
        McqAnswer.objects.create(
            answer=data[f'{q_number}_radio_option'], question=question)
        question.type = 'mcq'
        question.save()

    except KeyError:
        createCheckboxAnswers(data, q_number, question)


def createCheckboxAnswers(data, q_number, question):
    for j in range(1, len(data)):
        try:
            if data[f'{q_number}_checkbox_{j}'] == 'on':
                CheckboxAnswer.objects.create(
                    answer=j, question=question)
            question.type = 'checkbox'
            question.save()
        except KeyError:
            # pass cuz if 1_checkbox_1 doesnt exist i still need to check for 1_checkbox_2
            pass


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


def _addChoices(data, question, q_number, startIdx):
    for j in range(startIdx, len(data)):
        try:
            Choice.objects.create(
                choice=data[f'{q_number}_option{j}'], question=question)
        except KeyError:
            break


def _addNewCheckboxAnswers(data, question, q_number):
    for j in range(1, len(data)):
        try:
            if not CheckboxAnswer.objects.filter(answer=j, question=question).exists():
                if data[f'{q_number}_checkbox_{j}'] == 'on':
                    CheckboxAnswer.objects.create(
                        answer=j, question=question)
        except KeyError:
            pass


def _updateQuizTimer(data, quiz):
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


def _updateChoices(data, question, q_number):
    j = 1
    more_choices_left = True
    for choice in question.choice_set.all():
        try:
            choice.choice = data[f'{q_number}_option{j}']
            choice.save()
        except KeyError:
            choice.delete()
            more_choices_left = False
        j += 1

    if more_choices_left:
        _addChoices(data, question, q_number, j)


def _updateAnswers(data, question, q_number):
    if question.type == 'mcq':
        mcqanswer = question.mcqanswer
        mcqanswer.answer = data[f'{q_number}_radio_option']
        mcqanswer.save()

    elif question.type == 'checkbox':
        j = 1
        for answer in question.checkboxanswer_set.all():
            try:
                if data[f'{q_number}_checkbox_{answer.answer}'] == 'on':
                    pass

            except KeyError:
                answer.delete()
            j += 1

        _addNewCheckboxAnswers(data, question, q_number)


def _updateQuiz(data, quiz):
    quiz.name = data['quiz']

    _updateQuizTimer(data, quiz)

    q_number = 1
    more_questions_left = True
    for question in quiz.question_set.all():
        try:
            question.question = data[f'q_{q_number}']
            question.point = data[f'{q_number}_point']
            question.save()

            _updateChoices(data, question, q_number)

            _updateAnswers(data, question, q_number)

        except KeyError:
            question.delete()
            more_questions_left = False

        q_number += 1

    if more_questions_left:
        createQuestions(data, quiz, q_number)


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
            question=question, quiz=quiz, point=question.point, type=question.type)

        for choice in question.choice_set.all():
            Choice.objects.create(
                choice=choice, question=duplicate_question)

        if question.type == 'mcq':
            McqAnswer.objects.create(
                answer=question.mcqanswer.answer, question=duplicate_question)

        elif question.type == 'checkbox':
            for checboxAnswer in question.checkboxanswer_set.all():
                CheckboxAnswer.objects.create(
                    question=duplicate_question, answer=checboxAnswer.answer)

    return redirect('quiz-update', pk=quiz.id)


@login_required
def quizResult(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    if request.user != quiz.maker:
        raise PermissionDenied
    takers = quiz.taker_set.all()
    takers_list = list(takers.values())

    checkboxQuestions = [
        question for question in quiz.question_set.all() if question.type == 'checkbox']

    total = 0
    for question in quiz.question_set.all():
        total += question.point

    i = 0
    for taker in takers:
        mcqScore = getMcqQuestionsScore(quiz, taker)

        checkboxScore = getCheckboxQuestionsScore(checkboxQuestions, taker)

        score = mcqScore + checkboxScore

        takers_list[i]['score'] = f'{score}/{total}'
        i += 1

    return render(request, 'quiz/result.html', {'quiz': quiz, 'takers': takers_list})


def getMcqQuestionsScore(quiz, taker):
    mcqScore = 0

    for answer in taker.mcqanswer_set.all():
        if answer.quiz == quiz:
            point = answer.real_answer.question.point
            if answer.real_answer.answer == answer.answer:
                mcqScore += point

    return mcqScore


def getCheckboxQuestionsScore(checkboxQuestions, taker):
    for question in checkboxQuestions:
        real_answers = list(
            question.checkboxanswer_set.all())

        taker_total_correct_answers = 0
        checkboxScore = question.point

        answers = [answer for answer in taker.checkboxanswer_set.all()
                   if answer.question == question and answer.answer is not None]

        for answer in answers:

            if isTakerCheckboxAnswerCorrect(real_answers, answer):
                taker_total_correct_answers += 1
            else:
                checkboxScore = 0
                return checkboxScore

    if taker_total_correct_answers != len(real_answers):
        checkboxScore = 0

    return checkboxScore


def isTakerCheckboxAnswerCorrect(real_answers, answer):
    for real_answer in real_answers:
        if answer.answer == real_answer.answer:
            return True

    return False
