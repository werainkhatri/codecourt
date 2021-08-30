from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from problem.models import Problem, SampleTestCase


@login_required(login_url='login_n')
def problem(request, prob_id):
    problem = Problem.objects.get(id=prob_id)
    context = {
        'problem': problem,
        'samples': SampleTestCase.objects.filter(problem_id=problem.id)
        # 'samples': problem.sampletestcase_set.all(),
    }
    # if request.method == 'POST':
    return render(request, 'problem_page.html', context)
