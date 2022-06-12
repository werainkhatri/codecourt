from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from codecourt.settings import BASE_URL
from user.models import Submission


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if username == '' or email == '' or password1 == '' or password2 == '':
            messages.info(request, 'All fields are required')
            return redirect('register_n')
        elif password1 != password2:
            messages.info(request, 'Passwords don\'t matching')
            return redirect('register_n')
        else:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register_n')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('register_n')

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                messages.success(request, f'Account Created for {username}!')
                return redirect('login_n')

    else:
        context = {'title': 'Register - CodeCourt', 'BASE_URL': BASE_URL}
        return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, 'logged in')
            return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login_n')
    else:
        context = {'title': 'Login - CodeCourt', 'BASE_URL': BASE_URL}
        return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login_n')
def submissions(request):
    if request.method == 'POST':
        pass

    submissions = Submission.objects.filter(user=request.user).order_by('-id')
    context = {
        'title': 'Submissions - CodeCourt',
        'BASE_URL': BASE_URL,
        'submissions': submissions,
    }

    return render(request, 'submissions.html', context)
