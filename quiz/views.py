from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Quiz, Question, Choice, Answer
from django.views.decorators.http import require_POST


class QuizDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Quiz

    def test_func(self):
        return self.request.user == self.get_object().creator


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user).order_by('-id')
    # paginate_by = 100


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz-list')

    def test_func(self):
        return self.request.user == self.get_object().creator


@login_required
def newQuiz(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        user = request.user
        # print(user)
        quiz = Quiz.objects.create(name=data['quiz'], creator=user)
        # print(quiz)

        for i in range(1, len(data)):
            try:
                question = Question.objects.create(
                    question=data[f'q_{i}'], quiz=quiz, point=data[f'{i}_point'])

                # print(question.question)

                for j in range(1, 5):
                    Choice.objects.create(
                        choice=data[f'{i}_option{j}'], question=question)

                Answer.objects.create(
                    answer=data[f'{i}_radio_option'], question=question)

                # print(Question.objects.all())
                # print(Choice.objects.all())
                # print(Answer.objects.all())
            except Exception:
                break

        return redirect('quiz-list')

    defaultNumberOfChoices = range(1, 5)
    return render(request, 'quiz/new_quiz.html', {'defaultNumberOfChoices': defaultNumberOfChoices})


def updateQuiz(request, pk):
    if request.user != Quiz.objects.get(id=pk).creator:
        if request.user.is_anonymous:
            return redirect(f'/login/?next={request.path}')
        raise PermissionDenied

    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        user = request.user
        # print(user)
        quiz = Quiz.objects.get(id=pk)
        quiz.name = data['quiz']
        quiz.save()
        # print(quiz)

        i = 1
        for question in quiz.question_set.all():
            q_id = f'q_{question.id}'
            # print(q_id)
            question.question = data[f'q_{i}']
            question.point = data[f'{i}_point']
            question.save()
            # print(question)
            i += 1

            j = 1
            for choice in question.choice_set.all():
                choice.choice = data[f'{question.id}_option{j}']
                choice.save()
                j += 1

            answer = question.answer
            # print(answer)
            answer.answer = data[f'{question.id}_radio_option']
            answer.save()
            # print(answer)

        for k in range(i, len(data)):
            try:
                question = Question.objects.create(
                    question=data[f'q_{k}'], quiz=quiz, point=data[f'{k}_point'])
                # print(question)
                # print('here')
                # print(k)

                for j in range(1, len(data)):
                    try:
                        choice = Choice.objects.create(
                            choice=data[f'{k}_option{j}'], question=question)
                        # print(choice)
                    except Exception as e:
                        break

                Answer.objects.create(
                    answer=data[f'{k}_radio_option'], question=question)

            except Exception as e:
                break

        return redirect('quiz-list')

    quiz = Quiz.objects.get(id=pk)
    return render(request, 'quiz/quiz_update.html', {'quiz': quiz})


@require_POST
def quizDuplicate(request, pk):
    if request.user != Quiz.objects.get(id=pk).creator:
        # if request.user.is_anonymous:
        #     return redirect(f'/login/?next={request.path}')
        raise PermissionDenied

    data = request.POST.dict()
    parentQuiz = Quiz.objects.get(id=pk)
    quiz = Quiz.objects.create(name=data['quiz'], creator=request.user)
    for question in parentQuiz.question_set.all():
        duplicate_question = Question.objects.create(
            question=question, quiz=quiz)
        for choice in question.choice_set.all():
            Choice.objects.create(
                choice=choice, question=duplicate_question)
        Answer.objects.create(
            answer=question.answer.answer, question=duplicate_question)
    return redirect('quiz-detail', pk=quiz.id)


@login_required
def quizResult(request, pk):
    quiz = Quiz.objects.get(id=pk)
    print(request.user)
    if request.user != quiz.creator:
        raise PermissionDenied
    takers = quiz.taker_set.all()
    takers_list = list(takers.values())

    i = 0
    for taker in takers:
        score = 0
        total = 0
        for answer in taker.answer_set.all():
            if answer.quiz == quiz:
                point = answer.real_answer.question.point
                if answer.real_answer.answer == answer.answer:
                    score += point
                total += point

        takers_list[i]['score'] = f'{score}/{total}'
        i += 1

    return render(request, 'quiz/result.html', {'quiz': quiz, 'takers': takers_list})
