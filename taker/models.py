from django.db import models
import quiz.models as quiz_models
from quiz.utils.helpers import getFormattedScore


class Taker(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    USERNAME_FIELD = "email"
    quiz = models.ForeignKey(
        quiz_models.Quiz, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.email)

    @property
    def score(self):
        quizTotalPoints = self.quiz.totalPoints

        mcqScore = self._getMcqQuestionsScore()
        checkboxScore = self._getCheckboxQuestionsScore()
        score = mcqScore + checkboxScore

        return getFormattedScore(score, quizTotalPoints)

    def _getMcqQuestionsScore(self):
        return sum(takerAnswer.getScore() for takerAnswer in self.mcqanswer_set.all())

    def _getCheckboxQuestionsScore(self):
        checkboxQuestions = [question for question in self.quiz.question_set.all()
                             if question.type == 'checkbox']

        checkboxScore = sum(self._getCheckboxQuestionScore(
            question, question.point) for question in checkboxQuestions)

        return checkboxScore

    def _getCheckboxQuestionScore(self, question, questionPoints):
        realAnswers, takerAnswers = self._getCheckboxAnswersAndRealAnswers(
            question)

        if len(realAnswers) != len(takerAnswers):
            qScore = 0
            return qScore

        takerAnswers.sort()
        realAnswers.sort()

        qScore = questionPoints if takerAnswers == realAnswers else 0
        return qScore

    def _getCheckboxAnswersAndRealAnswers(self, question):
        realAnswers = [
            realAnswer.answer for realAnswer in question.checkboxanswer_set.all()]

        takerAnswers = [takerAnswer.answer for takerAnswer in self.checkboxanswer_set.all()
                        if takerAnswer.question == question and takerAnswer.answer is not None]

        return realAnswers, takerAnswers


class McqAnswer(models.Model):
    real_answer = models.ForeignKey(
        quiz_models.McqAnswer, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(Taker, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        quiz_models.Quiz, on_delete=models.CASCADE)
    answer = models.IntegerField(null=True)

    def __str__(self):
        return str(f'{self.answer} - {self.user} - {self.quiz}')

    def getScore(self):
        if self.real_answer.answer == self.answer:
            return self.real_answer.question.point
        else:
            return 0


class CheckboxAnswer(models.Model):
    user = models.ForeignKey(Taker, on_delete=models.CASCADE)
    question = models.ForeignKey(
        quiz_models.Question, on_delete=models.CASCADE, related_name='+')
    answer = models.IntegerField(null=True)

    def __str__(self):
        return str(f'{self.answer} - {self.user}')
