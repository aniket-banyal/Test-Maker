from datetime import datetime
from quiz.models import Quiz, Question, Choice, McqAnswer, CheckboxAnswer


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


def createQuestions(data, quiz, startIdx):
    for q_number in range(startIdx, len(data)):
        try:
            question = Question.objects.create(
                question=data[f'q_{q_number}'], quiz=quiz, point=data[f'{q_number}_point'])

            createChoices(data, q_number, question)
            createAnswers(data, q_number, question)

        except KeyError:
            break


def createChoices(data, q_number, question):
    for c_number in range(1, len(data)):
        try:
            Choice.objects.create(
                choice=data[f'{q_number}_option{c_number}'], question=question)
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
    for a_number in range(1, len(data)):
        try:
            if data[f'{q_number}_checkbox_{a_number}'] == 'on':
                CheckboxAnswer.objects.create(
                    answer=a_number, question=question)

            question.type = 'checkbox'
            question.save()

        except KeyError:
            # pass cuz if 1_checkbox_1 doesn't exist, still need to check for 1_checkbox_2
            pass
