from problem.models import Problem
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime as dt

class Submission(models.Model):

    JUDGEGCC = 'GNU GCC 9.3.0'
    JUDGEGPP = 'GNU G++ 9.3.0'
    JUDGEPYTHON = 'Python 3.8.0'

    VERDICT_CHOICES = (
        ('AC', 'accepted'),
        ('WA', 'wrong answer'),
        ('TE', 'time limit exceeded'),
        ('CE', 'compile error'),
        ('RE', 'runtime error'),
        ('TT', 'testing')
    )

    JUDGE_CHOICES = (
        (JUDGEGPP, 'g++'),
        (JUDGEGCC, 'gcc'),
        (JUDGEPYTHON, 'python')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    judge = models.CharField(max_length=30, choices=JUDGE_CHOICES)
    verdict = models.CharField(
        max_length=2, choices=VERDICT_CHOICES, default='TT')
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
