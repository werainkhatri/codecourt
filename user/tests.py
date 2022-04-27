from django.contrib.auth.models import User
from django.test import TestCase
from problem.constants import Judge

from problem.models import Problem, TestCase as tc
from user.models import Submission


class SubmissionTestCase(TestCase):
    def test_verdict_should_be_testing_when_created(self):
        problem = Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)
        user = User.objects.create(username='user1')
        submission = Submission.objects.create(
            user=user, problem=problem, code='code', judge=Judge.GCC)
        self.assertEquals(submission.verdict, 'TT')
        d = dict((x, y) for x, y in Submission.VERDICT_CHOICES)
        self.assertEquals(d[submission.verdict], 'testing')

    def test_verdict_should_be_accepted_when_judged_as_accepted(self):
        problem = Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)
        user = User.objects.create(username='user1')
        submission = Submission.objects.create(
            user=user, problem=problem, code='code', judge=Judge.GCC)
        submission.verdict = 'AC'
        submission.time = 1
        submission.memory = 1
        submission.save()
        self.assertEquals(submission.verdict, 'AC')
        d = dict((x, y) for x, y in Submission.VERDICT_CHOICES)
        self.assertEquals(d[submission.verdict], 'accepted')
