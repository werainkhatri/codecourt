from django.shortcuts import render
from problem.models import Problem


def problems(request):
    context = {
        'problems': Problem.objects.all(),
    }
    return render(request, 'problems.html', context)


def about(request):
    # TODO consider removing if not required
    return render(request, 'about.html', {'title': 'About_title'})
