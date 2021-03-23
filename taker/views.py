from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm
from quiz.models import Quiz
from .models import Taker, Answer
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz
import ssl
import smtplib
import threading


def takeQuizRegister(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # check if user has already taken quiz
            if Taker.objects.filter(email=user.email).exists():
                user = Taker.objects.get(email=user.email)
                if user.quiz == quiz:
                    return render(request, 'taker/already_taken_quiz.html')

            user.save()

            return redirect('take-quiz', pk=pk, user_id=user.id)

    else:
        form = UserRegisterForm()
        now = datetime.now().replace(tzinfo=pytz.UTC)
        endDateTime = quiz.startDateTime + timedelta(minutes=quiz.timeLimit)

        if endDateTime < now:
            return render(request, 'taker/quiz_not_accepting_responses.html')

    return render(request, 'taker/register.html', {'form': form})


def formatDateTimeJavascript(d):
    return datetime.strftime(d, '%d-%b-%Y %H:%M:%S')


def sendEmail(quiz, user):
    print("Sending mail")
    port = 465
    password = "You can't cracky m3!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sender_email = "fordblogging@gmail.com"
        server.login(sender_email, password)
        # receiver_email = "dummyani26@gmail.com"
        receiver_email = user.email

        msg = MIMEMultipart('alternative')

        text = f'Check out the correct answers to the quiz - {quiz.name}'

        html = f"""\
                <html>
                  <head></head>
                  <body>
                    <p>
                       Check out the correct answers to the quiz - {quiz.name} <br>
                       Here is the <a href='http://localhost:8000/take-quiz/{quiz.id}/{user.id}/result/'>link</a>.
                    </p>
                  </body>
                </html>
                """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        msg['Subject'] = 'Pro Quiz'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server.send_message(msg)
        server.quit()


@never_cache
def takeQuiz(request, pk, user_id):
    quiz = get_object_or_404(Quiz, id=pk)
    user = get_object_or_404(Taker, id=user_id)

    now = datetime.now().replace(tzinfo=pytz.UTC)
    startDateTime = quiz.startDateTime
    endDateTime = startDateTime + timedelta(minutes=quiz.timeLimit)

    print('\nstartDateTime- ', startDateTime)
    print('endDateTime-   ', endDateTime)
    print('datetime.now-  ', datetime.now(), '\n')

    if user.quiz == quiz:
        return render(request, 'taker/already_taken_quiz.html')

    if startDateTime > now:
        return render(request, 'taker/wait_for_quiz_start.html', {'startDateTime': formatDateTimeJavascript(startDateTime)})

    if endDateTime <= now:
        return render(request, 'taker/quiz_not_accepting_responses.html')

    context = {'quiz': quiz, 'user_id': user_id,
               'endDateTime': formatDateTimeJavascript(endDateTime)}
    return render(request, 'taker/take_quiz.html', context)


BUFFER_TIME = 5


@ require_POST
def submitQuiz(request, pk, user_id):
    quiz = get_object_or_404(Quiz, id=pk)
    user = get_object_or_404(Taker, id=user_id)

    if user.quiz == quiz:
        return render(request, 'taker/already_taken_quiz.html')

    now = datetime.now().replace(tzinfo=pytz.UTC)
    startDateTime = quiz.startDateTime
    endDateTime = startDateTime + timedelta(minutes=quiz.timeLimit)

    print('\nstartDateTime- ', startDateTime)
    print('endDateTime-   ', endDateTime)
    print('datetime.now-  ', datetime.now(), '\n')

    # if user manipulates seconds or minutes in console of take_quiz and submits after endDateTime, then to handle that
    if endDateTime + timedelta(seconds=BUFFER_TIME) < now:
        user.delete()
        return render(request, 'taker/quiz_not_accepting_responses.html')

    data = request.POST.dict()
    print(data)

    user.quiz = quiz
    user.save()

    for question in quiz.question_set.all():
        try:
            Answer.objects.create(answer=int(
                data[f'{question.id}_radio_option']), real_answer=question.answer, user=user, quiz=quiz)
        except KeyError:
            Answer.objects.create(
                real_answer=question.answer, user=user, quiz=quiz)

    if endDateTime < now:
        return redirect('result', pk=pk, user_id=user_id)

    else:
        print((endDateTime - now).total_seconds())

        timer = threading.Timer(
            (endDateTime - now).total_seconds(), sendEmail, args=[quiz, user])
        timer.start()

        return render(request, 'taker/quiz_submitted.html', {'user': user, 'endDate': endDateTime.date(), 'endTime': endDateTime.time()})


def result(request, pk, user_id):
    quiz = get_object_or_404(Quiz, id=pk)
    user = get_object_or_404(Taker, id=user_id)

    # if this url is visited by a logged in user who has not created this quiz deny
    # but still need to solve that anonymous user can still access this url
    if not request.user.is_anonymous:
        if request.user != quiz.maker:
            raise PermissionDenied

    total = 0
    for question in quiz.question_set.all():
        total += question.point

    score = 0
    for answer in user.answer_set.all():
        if answer.quiz == quiz:
            point = answer.real_answer.question.point
            if answer.real_answer.answer == answer.answer:
                score += point

    score = f'{score} / {total}'

    return render(request, 'taker/result.html', {'score': score, 'quiz': quiz, 'user': user})
