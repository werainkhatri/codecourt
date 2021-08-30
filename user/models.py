from problem.models import Problem
from django.contrib.auth.models import User
from django.db import models

class UserSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    time = models.DateTimeField(auto_now_add=True)