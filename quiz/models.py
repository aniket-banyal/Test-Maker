from django.db import models
from django.conf import settings
from django.urls import reverse


class Quiz(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.name} by {self.creator}'

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"pk": self.pk})
        # return reverse("quiz-detail", pk=self.pk)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    point = models.IntegerField()

    def __str__(self):
        return str(self.question)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=500)

    def __str__(self):
        return str(self.choice)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return str(self.answer)
