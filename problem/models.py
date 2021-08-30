from django.db import models
from django.contrib.auth.models import User


class Problem(models.Model):

    DIFFIULTY = (
        (0, 'EASY'),
        (1, 'MEDIUM'),
        (2, 'HARD')
    )

    name = models.CharField(max_length=100, unique=True)
    statement = models.TextField()
    difficulty = models.IntegerField(choices=DIFFIULTY, default=0)
    input = models.TextField(default='')
    output = models.TextField(default='')

    def __str__(self):
        return self.name


class SampleTestCase(models.Model):
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()


class HiddenTestCase(models.Model):
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()
