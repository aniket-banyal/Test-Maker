from taker.models import McqAnswer, CheckboxAnswer


def createTakerAnswers(quiz, user, data):
    for q_number, question in enumerate(quiz.question_set.all(), start=1):
        if question.type == 'mcq':
            try:
                answer = int(data[f'{q_number}_radio_option'])

            except KeyError:
                answer = None

            McqAnswer.objects.create(
                answer=answer, real_answer=question.mcqanswer, user=user, quiz=quiz)

        elif question.type == 'checkbox':
            for a_number in range(1, len(question.choice_set.all()) + 1):
                try:
                    if data[f'{q_number}_checkbox_{a_number}'] == 'on':
                        answer = a_number

                except KeyError:
                    answer = None

                CheckboxAnswer.objects.create(
                    answer=answer, user=user, question=question)
