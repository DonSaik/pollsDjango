from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import UserForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User, Group
# Create your views here.


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/polls')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def settings_view(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # for personnel in personnels:
            #     user = personnel.user
            #     if user.groups.filter(id=group.id).count():
            #         user.groups.remove(group)
            #     else:
            #         user.groups.add(group)
            return redirect('/polls')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'accounts/settings.html', {"form": form})


def logout_view(request):
    logout(request)

