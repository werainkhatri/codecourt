from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from problem.constants import Judge

from problem.models import Problem, TestCase as tc
from problem.views import run_testcases
from user.models import Submission
from user.views import submissions

class TestCaseTestCase(TestCase):
    def test_input_output_should_be_trimmed(self):
        problem = Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)
        test_case = tc.objects.create(
            problem_id=problem, is_sample=False, input=' input ', output=' output ')
        self.assertEqual(test_case.input, 'input')
        self.assertEqual(test_case.output, 'output')

    def test_is_sample_default_should_be_false(self):
        problem = Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)
        test_case = tc.objects.create(
            problem_id=problem, input=' input ', output=' output ')
        self.assertFalse(test_case.is_sample)

class ProblemTestCase(TestCase):
    def test_name_should_be_unique(self):
        Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)
        self.assertRaises(
            IntegrityError, Problem.objects.create,
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output', time_limit=1000)

    def test_time_limit_default_should_be_1000(self):
        problem = Problem.objects.create(
            name='problem1', statement='statement', difficulty=0,
            input='input', output='output')
        self.assertEqual(problem.time_limit, 1000)

class JudgeTestCase(TestCase):
    def test_python_correct_code(self):
        problem = Problem.objects.create(
            name='sum', statement='given two numbers, print their sum', difficulty=0,
            input='two numbers a and b', output='a + b')
        test_case1 = tc.objects.create(
            problem_id=problem, is_sample=False, input='5\n6', output='11')
        test_case2 = tc.objects.create(
            problem_id=problem, is_sample=False, input='10\n15', output='25')
        user = User.objects.create(username='user1')
        submission = Submission.objects.create(
            user=user, problem=problem, code='a=int(input())\nb=int(input())\nprint(a+b)', judge=Judge.PY3)
        
        run_testcases(submission, [test_case1, test_case2])

        self.assertEquals(submission.verdict, 'AC')

    def test_python_incorrect_code(self):
        problem = Problem.objects.create(
            name='sum', statement='given two numbers, print their sum', difficulty=0,
            input='two numbers a and b', output='a + b')
        test_case1 = tc.objects.create(
            problem_id=problem, is_sample=False, input='5\n6', output='11')
        test_case2 = tc.objects.create(
            problem_id=problem, is_sample=False, input='10\n15', output='25')
        user = User.objects.create(username='user1')
        submission = Submission.objects.create(
            user=user, problem=problem, code='a=int(input())\nb=int(input())\nprint(a-b)', judge=Judge.PY3)
        
        run_testcases(submission, [test_case1, test_case2])

        self.assertEquals(submission.verdict, 'WA')
        
