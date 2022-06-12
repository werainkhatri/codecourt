from django.shortcuts import render
from codecourt.settings import BASE_URL
from problem.models import Problem


def problems(request):
    context = {
        'problems': Problem.objects.all(),
        'BASE_URL': BASE_URL,
    }
    return render(request, 'problems.html', context)
