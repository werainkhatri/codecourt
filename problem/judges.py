import os, tarfile
import subprocess as sp
from time import time
import docker

from user.models import Submission
from . import constants as _

__client = docker.from_env()

def judge_gcc(submission: Submission):
    '''
    Tests submission against the gcc judge
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        ext=_.C,
        compile='gcc -o {} {}.c'.format(filename, filename),
        run='./{}'.format(filename),
        clear='rm {} {}.c'.format(filename, filename)
    )


def judge_gpp(submission: Submission):
    '''
    Tests submission against the gpp judge
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        ext=_.CPP,
        compile='g++ -o {} {}.cpp'.format(filename, filename),
        run='./{}'.format(filename),
        clear='rm {} {}.cpp'.format(filename, filename)
    )


def judge_python(submission: Submission):
    '''
    Tests submission against the python judge
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        ext=_.PY,
        run='python {}.py'.format(filename),
        clear='rm {}.py'.format(filename)
    )



def __chief_judge(submission, ext, clear, run, compile=None):
    filename = str(submission.id) + '.' + ext
    hostfile = _.CODES_DIR + filename

    file = open(hostfile, 'xt')
    file.write(submission.code)
    file.close()
    
    container: docker.models.containers.Container = None
    try:
        container = __client.containers.get(_.CONTAINER_NAME[ext])
    except docker.errors.NotFound:
        container = __client.containers.run(_.DOCKER_IMAGE[ext],
            stdin_open=True, 
            detach=True, 
            tty=True,
            name=_.CONTAINER_NAME[ext])
    
    __copy_to(hostfile, filename, container)

    maxtime = 0.0
    verdict = 'AC'

    def close():
        sp.run(['rm', filename])
        sp.run(['rm', filename+'.tar'])
        # sp.run('docker exec ' + _.CONTAINER_NAME[ext] + ' ' + clear, shell=True)
        return {'verdict': verdict, 'time': maxtime}

    if compile:
        cp = sp.run('docker exec ' +  _.CONTAINER_NAME[ext] + ' ' + compile, shell=True)
        if cp.returncode != 0:
            verdict = 'CE'
            return close()

    
    for tc in submission.problem.testcase_set.all():
        start = time()

        try:
            cp = sp.run('docker exec ' + _.CONTAINER_NAME[ext] + ' sh -c \'echo "{}" | {}\''.format(tc.input, run),
                    shell=True,
                    capture_output=True,
                    timeout=submission.problem.time_limit / 1000)
        except sp.TimeoutExpired:
            maxtime = (time() - start) * 1000
            verdict = 'TE'
            break
        
        maxtime = max(maxtime, (time() - start) * 1000)

        if cp.returncode != 0:
            print(cp.stderr.decode())
            verdict = 'RE'
            break

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        if not useroutput == tc.output:
            verdict = 'WA'
            break
    
    return close()

def __copy_to(src, dst, container):
    src = '/home/werain/dev/dj/CodeCourt/' + src
    dst = '/' + dst
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()
    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
