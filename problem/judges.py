import subprocess as sp
from time import time

from user.models import Submission

from problem.models import Problem

CODES_DIR = 'session/'


def judge_gcc(submission: Submission):
    '''
    Tests submission against the gcc judge
    '''
    return __judge_gxx(submission, 'gcc', 'c')


def judge_gpp(submission: Submission):
    '''
    Tests submission against the gpp judge
    '''
    return __judge_gxx(submission, 'g++', 'cpp')


def judge_python(submission: Submission):
    '''
    Tests submission against the python judge
    '''
    filename = str(submission.id)

    file = open(CODES_DIR + filename + '.py', 'xt')
    file.write(submission.code)
    file.close()

    def delete_file():
        sp.run(['rm', '{}{}.py'.format(CODES_DIR, filename)])
    
    maxtime = 0.0
    for tc in submission.problem.testcase_set.all():
        start = time()
        try:
            cp = sp.run(['python', '{}{}.py'.format(CODES_DIR, filename)],
                            input=tc.input.encode(),
                            capture_output=True,
                            timeout=submission.problem.time_limit)
        except sp.TimeoutExpired:
            delete_file()
            return {'verdict': 'TE', 'time': (time() - start) * 1000}
        
        maxtime = max(maxtime, (time() - start) * 1000)

        if cp.returncode != 0:
            delete_file()
            print(cp.stderr.decode())
            return {'verdict': 'RE', 'time': maxtime}

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        if not useroutput == tc.output:
            delete_file()
            return {'verdict': 'WA', 'time': maxtime}
    
    delete_file()
    return {'verdict': 'AC', 'time': maxtime}


def __judge_gxx(submission: Submission, compiler, ext):
    filename = str(submission.id)

    file = open(CODES_DIR + filename + '.{}'.format(ext), 'xt')
    file.write(submission.code)
    file.close()

    # Compile
    cp = sp.run([compiler, '-o', CODES_DIR + filename, '{}{}.{}'.format(CODES_DIR, filename, ext)])
    # Delete code file
    sp.run(['rm', '{}{}.{}'.format(CODES_DIR, filename, ext)])

    def delete_file():
        sp.run(['rm', '{}{}'.format(CODES_DIR, filename)])
    
    if(cp.returncode != 0):
        return {'verdict': 'CE', 'time': 0}

    maxtime = 0.0
    for tc in submission.problem.testcase_set.all():
        start = time()
        try:
            cp = sp.run('./{}{}'.format(CODES_DIR, filename),
                            input=tc.input.encode(),
                            capture_output=True,
                            timeout=submission.problem.time_limit)
        except sp.TimeoutExpired:
            delete_file()
            return {'verdict': 'TE', 'time': (time() - start) * 1000}
        
        maxtime = max(maxtime, (time() - start) * 1000)

        if cp.returncode != 0:
            delete_file()
            return {'verdict': 'RE', 'time': maxtime}

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        if not useroutput == tc.output:
            delete_file()
            return {'verdict': 'WA', 'time': maxtime}
    
    delete_file()
    return {'verdict': 'AC', 'time': maxtime}
