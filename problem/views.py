from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import subprocess as sb
from multiprocessing import Process
from time import time

from problem.models import Problem, TestCase
from user.models import Submission

COMPILER_DICT = dict((x, y) for x, y in Submission.LANGUAGE_CHOICES)

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
                                lang=request.POST['language'])
        submission.save()
        p = Process(target=run_testcases, args=(submission,))
        p.start()
        return redirect('submissions')

    context = {
        'problem': problem,
        'samples': TestCase.objects.filter(problem_id=problem.id, is_sample=True),
        'langs': Submission.LANGUAGE_CHOICES,
    }
    return render(request, 'problem.html', context)


def run_testcases(submission: Submission):
    compiler = COMPILER_DICT[submission.lang]
    extention = EXTENTION_DICT[compiler]
    runner = compiler + ' '

    # Load code
    file = open('code/' + FILE_NAME + '.' + extention, 'wt')
    file.write(submission.code)
    file.close()

    output = None

    if IS_COMPILED[extention]:
        if(not compile_code(compiler, extention)):
            output = {'verdict': 'CE', 'time': 0}
        else:
            # since compilation is successful, we can change the extention
            # so that the tests are done against the output file
            extention = 'out' + extention
            runner = "./"

    # an interpreted language would jump directly here
    if not output:
        output = test_code(submission.problem, runner, extention)

    submission.verdict = output['verdict']
    submission.time = output['time']
    # TODO find a way to calculate memory
    submission.save()


def compile_code(compiler, extention):
    """
    Compiles the file "`FILE_NAME`.`extention`" with the given `compiler`
    and produces the output file as "`FILE_NAME`.out`extention`"
    """
    cp = sb.run('cd code && ' +
                compiler + ' -o ' + FILE_NAME + '.out' + extention + ' ' +
                FILE_NAME + '.' + extention,
                shell=True, capture_output=True)
    return cp.returncode == 0


def test_code(problem: Problem, runner, extention):
    maxtime = 0

    for tc in problem.testcase_set.all():
        start_time = time()
        try:
            cp = sb.run(runner + 'code/' + FILE_NAME + '.' + extention,
                        shell=True,
                        input=tc.input.encode(),
                        capture_output=True,
                        timeout=problem.time_limit/1000)
        except sb.TimeoutExpired:
            return {'verdict': 'TE', 'time': (time() - start_time)*1000}

        maxtime = (time()-start_time)*1000

        if maxtime > 1000:
            return {'verdict': 'TE', 'time': maxtime}

        if cp.returncode != 0:
            return {'verdict': 'RE', 'time': maxtime}

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        if not useroutput == tc.output:
            return {'verdict': 'WA', 'time': maxtime}

    return {'verdict': 'AC', 'time': maxtime}
