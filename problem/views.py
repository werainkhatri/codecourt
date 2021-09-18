from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import subprocess as sb
from multiprocessing import Process
from time import time

from .models import Problem, TestCase
from .judges import judge_gcc, judge_gpp, judge_python
from user.models import Submission

COMPILER_DICT = dict((x, y) for x, y in Submission.JUDGE_CHOICES)

EXTENTION_DICT = {
    'g++': 'cpp',
    'gcc': 'c',
    'python': 'py',
}

# If the language associated with input extention
# is compiled (True) or interpreted (False)
IS_COMPILED = {
    'cpp': True,
    'c': True,
    'py': False,
}

FILE_NAME = 'in'


@login_required(login_url='login_n')
def problem(request, prob_id):
    problem = Problem.objects.get(id=prob_id)

    if request.method == 'POST':
        submission = Submission(user=request.user,
                                problem=problem,
                                code=request.POST['code'],
                                judge=request.POST['language'])
        submission.save()
        p = Process(target=run_testcases, args=(submission,))
        p.start()
        return redirect('submissions')

    context = {
        'problem': problem,
        'samples': TestCase.objects.filter(problem_id=problem.id, is_sample=True),
        'judges': Submission.JUDGE_CHOICES,
    }
    return render(request, 'problem.html', context)


def run_testcases(submission: Submission):
    if submission.judge == Submission.JUDGEGCC:
        output = judge_gcc(submission)
    elif submission.judge == Submission.JUDGEGPP:
        output = judge_gpp(submission)
    elif submission.judge == Submission.JUDGEPYTHON:
        output = judge_python(submission)

    submission.verdict = output['verdict']
    submission.time = output['time']
    # TODO find a way to calculate memory
    submission.save()
