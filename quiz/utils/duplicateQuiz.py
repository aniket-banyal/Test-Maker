from quiz.models import Quiz, Question, Choice, McqAnswer, CheckboxAnswer


def duplicateQuiz(user, parentQuiz, duplicateQuizName):
    quiz = Quiz.objects.create(maker=user, name=duplicateQuizName, startDateTime=parentQuiz.startDateTime,
                               timeLimit=parentQuiz.timeLimit)

    duplicateQuestions(parentQuiz.question_set.all(), quiz)

    return quiz


def duplicateQuestions(parentQuestions, quiz):
    for parentQuestion in parentQuestions:
        duplicateQuestion = Question.objects.create(quiz=quiz, question=parentQuestion.question,
                                                    point=parentQuestion.point, type=parentQuestion.type)

        duplicateChoices(parentQuestion.choice_set.all(), duplicateQuestion)
        duplicateAnswers(parentQuestion, duplicateQuestion)


def duplicateChoices(parentChoices, duplicateQuestion):
    for parentChoice in parentChoices:
        Choice.objects.create(question=duplicateQuestion,
                              choice=parentChoice.choice)


def duplicateAnswers(parentQuestion, duplicateQuestion):
    if parentQuestion.type == 'mcq':
        McqAnswer.objects.create(question=duplicateQuestion,
                                 answer=parentQuestion.mcqanswer.answer)

    elif parentQuestion.type == 'checkbox':
        for checkboxAnswer in parentQuestion.checkboxanswer_set.all():
            CheckboxAnswer.objects.create(question=duplicateQuestion,
                                          answer=checkboxAnswer.answer)
