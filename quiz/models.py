from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta
import pytz


class Quiz(models.Model):
    maker = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    startDateTime = models.DateTimeField(null=True)
    timeLimit = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"pk": self.pk})
        # return reverse("quiz-detail", pk=self.pk)

    @property
    def endDateTime(self):
        return self.startDateTime + timedelta(minutes=self.timeLimit)

    def hasStarted(self):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        return now > self.startDateTime

    def isOver(self):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        return now >= self.endDateTime

    def getStartDate(self, dateFormat='%Y-%m-%d'):
        startDateTime = self.startDateTime

        if startDateTime is not None:
            startDate = startDateTime.date().strftime(dateFormat)
        else:
            startDate = None

        return startDate

    def getStartTime(self, timeFormat='%H:%M'):
        startDateTime = self.startDateTime

        if startDateTime is not None:
            startTime = startDateTime.time().strftime(timeFormat)
        else:
            startTime = None

        return startTime

    @property
    def totalPoints(self):
        return sum(question.point for question in self.question_set.all())


class QuestionManager(models.Manager):
    def mcq_questions(self):
        return self.get_queryset().filter(type='mcq')

    def checkbox_questions(self):
        return self.get_queryset().filter(type='checkbox')

    def short_questions(self):
        return self.get_queryset().filter(type='short')


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    point = models.IntegerField()
    type = models.CharField(max_length=20, null=True)

    objects = QuestionManager()

    def __str__(self):
        return str(self.question)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=500)

    def __str__(self):
        return str(self.choice)


class McqAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return str(self.answer)


class CheckboxAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return str(self.answer)


class ShortAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return str(self.answer)
