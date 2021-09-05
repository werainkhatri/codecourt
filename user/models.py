from problem.models import Problem
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime as dt


class Submission(models.Model):

    VERDICT_CHOICES = (
        ('AC', 'accepted'),
        ('WA', 'wrong answer'),
        ('TE', 'time limit exceeded'),
        ('CE', 'compile error'),
        ('RE', 'runtime error'),
        ('TT', 'testing')
    )

    LANGUAGE_CHOICES = (
        ('GNU G++ 9.3.0', 'g++'),
        ('GNU GCC 9.3.0', 'gcc'),
        ('Python 3.8.10', 'python')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    lang = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default=1)
    verdict = models.CharField(
        max_length=2, choices=VERDICT_CHOICES, default='TT')
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
