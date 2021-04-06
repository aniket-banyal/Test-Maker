from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from quiz import views as quiz_views
from maker import views as maker_views
from taker import views as taker_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', maker_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='maker/login.html'), name='login'),
    path('', quiz_views.QuizListView.as_view(), name='quiz-list'),
    path('quiz/<int:pk>/', quiz_views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:pk>/update/', quiz_views.updateQuiz, name='quiz-update'),
    path('quiz/<int:pk>/delete/', quiz_views.QuizDeleteView.as_view(), name='quiz-delete'),
    path('quiz/new/', quiz_views.newQuiz, name='new-quiz'),
    path('quiz/<int:pk>/duplicate/', quiz_views.quizDuplicate, name='quiz-duplicate'),
    path('quiz/<int:pk>/result/', quiz_views.quizResult, name='quiz-result'),
    path('take-quiz/<int:pk>/register/', taker_views.takeQuizRegister,name='take-quiz-register'),
    path('take-quiz/<int:pk>/<int:taker_id>/', taker_views.takeQuiz,name='take-quiz'),
    path('take-quiz/<int:pk>/<int:taker_id>/submit/', taker_views.submitQuiz, name='submit-quiz'),
    path('take-quiz/<int:pk>/<int:taker_id>/result/', taker_views.result, name='result'),
]
