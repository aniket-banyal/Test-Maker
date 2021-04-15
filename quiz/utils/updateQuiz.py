from datetime import datetime
from quiz.models import Choice, CheckboxAnswer, ShortAnswer
from quiz.utils.createQuiz import createQuestions


def _updateQuiz(data, quiz):
    quiz.name = data['quiz']
    quiz.save()

    updateQuizTimer(data, quiz)

    more_questions_left = True
    for q_number, question in enumerate(quiz.question_set.all(), start=1):
        try:
            question.question = data[f'q_{q_number}']
            question.point = data[f'{q_number}_point']
            question.save()

            updateChoices(data, question, q_number)
            updateAnswers(data, question, q_number)

        except KeyError:
            question.delete()
            more_questions_left = False

    if more_questions_left:
        createQuestions(data, quiz, q_number+1)


def updateQuizTimer(data, quiz):
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


def updateChoices(data, question, q_number):
    if question.type == 'short':
        return updateShortAnswers(question, data, q_number)

    more_choices_left = True
    for c_number, choice in enumerate(question.choice_set.all(), start=1):
        try:
            choice.choice = data[f'{q_number}_option{c_number}']
            choice.save()

        except KeyError:
            choice.delete()
            more_choices_left = False

    if more_choices_left:
        addNewChoices(data, question, q_number, c_number + 1)


def updateShortAnswers(question, data, q_number):
    more_answers_left = True

    for a_number, shortAnswer in enumerate(question.shortanswer_set.all(), start=1):
        try:
            shortAnswer.answer = data[f'{q_number}_short_{a_number}']
            shortAnswer.save()

        except KeyError:
            shortAnswer.delete()
            more_answers_left = False

    if more_answers_left:
        addNewShortAnswers(data, question, q_number, a_number + 1)


def addNewShortAnswers(data, question, q_number, startIdx):
    for a_number in range(startIdx, len(data)):
        try:
            ShortAnswer.objects.create(
                answer=data[f'{q_number}_short_{a_number}'], question=question)

        except KeyError:
            break


def updateAnswers(data, question, q_number):
    if question.type == 'mcq':
        mcqanswer = question.mcqanswer
        mcqanswer.answer = data[f'{q_number}_radio_option']
        mcqanswer.save()

    elif question.type == 'checkbox':
        for answer in question.checkboxanswer_set.all():
            try:
                if data[f'{q_number}_checkbox_{answer.answer}'] == 'on':
                    pass

            except KeyError:
                answer.delete()

        addNewCheckboxAnswers(data, question, q_number)


def addNewChoices(data, question, q_number, startIdx):
    for c_number in range(startIdx, len(data)):
        try:
            Choice.objects.create(
                choice=data[f'{q_number}_option{c_number}'], question=question)

        except KeyError:
            break


def addNewCheckboxAnswers(data, question, q_number):
    for a_number in range(1, len(data)):
        try:
            if not CheckboxAnswer.objects.filter(answer=a_number, question=question).exists():
                if data[f'{q_number}_checkbox_{a_number}'] == 'on':
                    CheckboxAnswer.objects.create(
                        answer=a_number, question=question)

        except KeyError:
            pass
