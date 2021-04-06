from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import Quiz
from quiz.utils.createQuiz import createQuiz
from quiz.utils.updateQuiz import _updateQuiz
from quiz.utils.duplicateQuiz import duplicateQuiz


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


@login_required
def newQuiz(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)

        createQuiz(data, request.user)

        return redirect('quiz-list')

    defaultNumberOfChoices = range(1, 5)
    return render(request, 'quiz/new_quiz.html', {'defaultNumberOfChoices': defaultNumberOfChoices})


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

    startDate = quiz.getStartDate()
    startTime = quiz.getStartTime()

    return render(request, 'quiz/quiz_update.html', {'quiz': quiz, 'startDate': startDate, 'startTime': startTime})


@require_POST
def quizDuplicate(request, pk):
    parentQuiz = get_object_or_404(Quiz, id=pk)

    if request.user != parentQuiz.maker:
        raise PermissionDenied

    data = request.POST.dict()

    quiz = duplicateQuiz(request.user, parentQuiz, data['quiz'])

    return redirect('quiz-update', pk=quiz.id)


@login_required
def quizResult(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.user != quiz.maker:
        raise PermissionDenied

    takers = quiz.taker_set.all()
    return render(request, 'quiz/result.html', {'quiz': quiz, 'takers': takers})
