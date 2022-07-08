import subprocess as sp
from time import time

import docker
from docker.models.containers import Container
from user.models import Submission

from . import constants as _

__client = docker.from_env()


def judge_gcc(submission: Submission, testcases):
    '''
    Tests `submission` against the gcc judge
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        testcases=testcases,
        ext='c',
        compile='gcc -o {} {}.c'.format(filename, filename),
        run='./{}'.format(filename),
        clear='rm {} {}.c'.format(filename, filename),
        cont_name=_.Judge.GCCCONT,
        docker_image=_.Judge.GCCIMG,
    )


def judge_gpp(submission: Submission, testcases, std: str):
    '''
    Tests `submission` against the g++ judge,
    and `std` standard
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        testcases=testcases,
        ext="cpp",
        compile='g++ -std=c++{} -o {} {}.cpp'.format(std, filename, filename),
        run='./{}'.format(filename),
        clear='rm {} {}.cpp'.format(filename, filename),
        cont_name=_.Judge.GCCCONT,
        docker_image=_.Judge.GCCIMG,
    )


def judge_python(submission: Submission, testcases, is3: bool):
    '''
    Tests `submission` against the python judge.
    if `is3`, it will be against python 3, else python 2
    '''
    filename = str(submission.id)

    return __chief_judge(
        submission=submission,
        testcases=testcases,
        ext='py',
        run='python {}.py'.format(filename),
        clear='rm {}.py'.format(filename),
        cont_name=_.Judge.PY3CON if is3 else _.Judge.PY2CON,
        docker_image=_.Judge.PY3IMG if is3 else _.Judge.PY2IMG,
    )


def __chief_judge(submission, testcases, ext, clear, run, cont_name, docker_image, compile=None):
    filename = str(submission.id) + '.' + ext
    hostfile = _.CODES_DIR + filename

    file = open(_.HOST_PATH + hostfile, 'w+')
    file.write(submission.code)
    file.close()

    container: docker.models.containers.Container = None
    try:
        container: Container = __client.containers.get(cont_name)
        if(container.status != 'running'):
            container.start()
    except docker.errors.NotFound:
        container = __client.containers.run(docker_image,
                                            stdin_open=True,
                                            detach=True,
                                            tty=True,
                                            name=cont_name)

    __copy_to_container(hostfile, filename, container)

    maxtime = 0.0
    verdict = 'AC'

    def close():
        sp.run(['rm', hostfile])
        sp.run('docker exec ' + cont_name + ' ' + clear, shell=True)
        return {'verdict': verdict, 'time': maxtime}

    if compile:
        cp = sp.run('docker exec ' + cont_name + ' ' + compile, shell=True)
        if cp.returncode != 0:
            verdict = 'CE'
            return close()

    for tc in testcases:
        start = time()

        try:
            cp = sp.run('docker exec ' + cont_name + ' sh -c \'echo "{}" | {}\''.format(tc.input, run),
                        shell=True,
                        capture_output=True,
                        timeout=submission.problem.time_limit / 1000)
        except sp.TimeoutExpired:
            maxtime = (time() - start) * 1000
            verdict = 'TE'
            break

        maxtime = max(maxtime, (time() - start) * 1000)

        if cp.returncode != 0:
            verdict = 'RE'
            break

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        if not useroutput == tc.output:
            verdict = 'WA'
            break

    return close()


def __copy_to_container(src, dst, container):
    src = _.HOST_PATH + src
    dst = _.CONT_PATH + dst
    sp.run(['docker', 'cp', src, container.id+':'+dst])
