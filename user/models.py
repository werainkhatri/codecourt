from django.contrib.auth.models import User
from django.db import models
from problem.constants import MAX_CODE_LENGTH, Judge
from problem.models import Problem


class Submission(models.Model):

    VERDICT_CHOICES = (
        ('AC', 'accepted'),
        ('WA', 'wrong answer'),
        ('TE', 'time limit exceeded'),
        ('CE', 'compile error'),
        ('RE', 'runtime error'),
        ('TT', 'testing')
    )

    JUDGE_CHOICES = (
        # (1, Judge.PY2),
        (2, Judge.PY3),
        (3, Judge.GCC),
        (4, Judge.GPP14),
        (5, Judge.GPP17),
        (6, Judge.GPP20),
        # (7, Judge.JAVA8),
        # (8, Judge.JAVA11),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField(max_length=MAX_CODE_LENGTH)
    datetime = models.DateTimeField(auto_now_add=True)
    judge = models.CharField(max_length=30, choices=JUDGE_CHOICES)
    verdict = models.CharField(
        max_length=2, choices=VERDICT_CHOICES, default='TT')
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
