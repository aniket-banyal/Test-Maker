from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            print(email)
            new_user = authenticate(
                email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            # login(request, new_user)
            return redirect('quiz-list')
    else:
        form = UserRegisterForm()
    return render(request, 'maker/register.html', {'form': form})
