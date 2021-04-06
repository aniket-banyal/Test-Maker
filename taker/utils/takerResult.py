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
