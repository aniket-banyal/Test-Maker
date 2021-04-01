from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .forms import UserRegisterForm
from quiz.models import Quiz
from .models import Taker, McqAnswer, CheckboxAnswer
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
                for existing_taker in Taker.objects.filter(email=user.email):
                    if existing_taker.quiz == quiz:
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

    createTakerAnswers(quiz, user, data)

    if endDateTime < now:
        return redirect('result', pk=pk, user_id=user_id)

    else:
        print((endDateTime - now).total_seconds())

        timer = threading.Timer(
            (endDateTime - now).total_seconds(), sendEmail, args=[quiz, user])
        timer.start()

        return render(request, 'taker/quiz_submitted.html', {'user': user, 'endDate': endDateTime.date(), 'endTime': endDateTime.time()})


def createTakerAnswers(quiz, user, data):
    i = 1

    for question in quiz.question_set.all():
        if question.type == 'mcq':
            try:
                McqAnswer.objects.create(answer=int(
                    data[f'{i}_radio_option']), real_answer=question.mcqanswer, user=user, quiz=quiz)
            except KeyError:
                McqAnswer.objects.create(
                    real_answer=question.mcqanswer, user=user, quiz=quiz)

        elif question.type == 'checkbox':
            for j in range(1, len(question.choice_set.all()) + 1):
                try:
                    if data[f'{i}_checkbox_{j}'] == 'on':
                        CheckboxAnswer.objects.create(
                            answer=j, user=user, question=question)
                except KeyError:
                    CheckboxAnswer.objects.create(user=user, question=question)
        i += 1


def result(request, pk, user_id):
    quiz = get_object_or_404(Quiz, id=pk)
    user = get_object_or_404(Taker, id=user_id)

    # if this url is visited by a logged in user who has not created this quiz deny
    # but still need to solve that anonymous user can still access this url
    if not request.user.is_anonymous:
        if request.user != quiz.maker:
            raise PermissionDenied

    allQuestions = quiz.question_set.all()

    total = 0
    for question in allQuestions:
        total += question.point

    takerQuestions = createTakerQuestionsList(
        allQuestions, user)

    checkboxQuestions = [
        question for question in allQuestions if question.type == 'checkbox']

    mcqScore = getMcqQuestionsScore(quiz, user)
    checkboxScore = getCheckboxQuestionsScore(checkboxQuestions, user)

    score = mcqScore + checkboxScore
    score = f'{score} / {total}'

    return render(request, 'taker/result.html', {'score': score, 'quiz': quiz, 'user': user, 'questions': takerQuestions})


class TakerQuestion:
    def __init__(self, question, point, type, choices=[]):
        self.question = question
        self.point = point
        self.type = type
        self.choices = choices


class TakerChoice:
    def __init__(self, choice, isAnswer=False, isMarkedByTaker=False, css_class=None):
        self.choice = choice
        self.isAnswer = isAnswer
        self.isMarkedByTaker = isMarkedByTaker
        self.css_class = css_class


def createTakerQuestionsList(questions, taker):
    t_questions = []

    for question in questions:
        t_question = TakerQuestion(
            question.question, question.point, question.type)

        t_question.choices = getTakerQuestionChoices(question, taker)

        t_questions.append(t_question)

    return t_questions


def getTakerQuestionChoices(question, taker):
    choices = []
    choice_number = 1

    for choice in question.choice_set.all():
        taker_choice = TakerChoice(
            choice.choice, isAnswer=isChoiceAnswer(question, choice_number))

        taker_choice.isMarkedByTaker = isChoiceMarkedByTaker(
            taker, question, choice_number)

        taker_choice.css_class = getTakerChoiceClass(taker_choice)

        choices.append(taker_choice)

        choice_number += 1

    return choices


def isChoiceAnswer(question, choice_number):
    if question.type == 'mcq':
        return choice_number == question.mcqanswer.answer

    elif question.type == 'checkbox':
        for answer in question.checkboxanswer_set.all():
            if choice_number == answer.answer:
                return True

        return False


def isChoiceMarkedByTaker(taker, question, choice_number):
    if question.type == 'mcq':
        t_answers = [t_answer for t_answer in taker.mcqanswer_set.all(
        ) if t_answer.real_answer == question.mcqanswer]

    elif question.type == 'checkbox':
        t_answers = [t_answer for t_answer in taker.checkboxanswer_set.all(
        ) if t_answer.question == question]

    for t_answer in t_answers:
        if t_answer.answer == choice_number:
            return True

    return False


def getTakerChoiceClass(taker_choice):
    css_class = None

    if taker_choice.isMarkedByTaker and taker_choice.isAnswer:
        css_class = 'correct'

    elif taker_choice.isMarkedByTaker and not taker_choice.isAnswer:
        css_class = 'wrong'

    elif not taker_choice.isMarkedByTaker and taker_choice.isAnswer:
        css_class = 'real-correct'

    return css_class


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
