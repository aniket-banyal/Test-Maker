from django.db import models
import quiz.models as quiz_models


class Taker(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    USERNAME_FIELD = "email"
    quiz = models.ForeignKey(
        quiz_models.Quiz, on_delete=models.CASCADE, null=True)


class Answer(models.Model):
    real_answer = models.ForeignKey(
        quiz_models.Answer, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(Taker, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        quiz_models.Quiz, on_delete=models.CASCADE)

    answer = models.IntegerField()
