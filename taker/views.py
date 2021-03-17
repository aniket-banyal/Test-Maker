from django.core.exceptions import PermissionDenied
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from quiz.models import Quiz, Question
from .models import Taker, Answer


def takeQuiz(request, pk):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            quiz = Quiz.objects.get(id=pk)
            user = form.save(commit=False)

            # check if user has already taken quiz
            if Taker.objects.filter(email=user.email).exists():
                user = Taker.objects.get(email=user.email)
                print(user.quiz, quiz)
                if user.quiz == quiz:
                    return HttpResponse('You have already taken this quiz')

            user.save()

            context = {'quiz': quiz, 'user_id': user.id}
            return render(request, 'taker/take_quiz.html', context)
    else:
        form = UserRegisterForm()
    return render(request, 'taker/register.html', {'form': form})


@require_POST
def submitQuiz(request, pk, user_id):
    if request.method == 'POST':

        quiz = Quiz.objects.get(id=pk)
        user = Taker.objects.get(id=user_id)

        if user.quiz == quiz:
            return HttpResponse('You have already taken this quiz')

        user.quiz = quiz
        user.save()

        # print(user.email, user.name)

        data = request.POST.dict()
        print(data)
        data = {key: val for key, val in data.items(
        ) if key.endswith('radio_option')}
        print(data)

        for x in list(data.keys()):
            q_id = [int(s) for s in x.split('_') if s.isdigit()][0]
            print(q_id)
            question = Question.objects.get(id=q_id)
            Answer.objects.create(answer=int(
                data[x]), real_answer=question.answer, user=user, quiz=quiz)

        return redirect('result', pk=pk, user_id=user_id)


def result(request, pk, user_id):
    print(request.user)
    quiz = Quiz.objects.get(id=pk)

    # if this url is visited by a loggen in user who has not created this quiz deny
    # but still need to solve that anonymous user can still access this url
    if not request.user.is_anonymous:
        if request.user != quiz.creator:
            raise PermissionDenied

    user = Taker.objects.get(id=user_id)

    score = 0
    total = 0
    for answer in user.answer_set.all():
        if answer.quiz == quiz:
            if answer.real_answer.answer == answer.answer:
                score += 1
            total += 1

    score = f'{score} / {total}'

    return render(request, 'taker/result.html', {'score': score, 'quiz': quiz, 'user': user})
