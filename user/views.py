from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import user
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.profile.birthdate = p_form.cleaned_data.get('birthdate')
            user.profile.gender = p_form.cleaned_data.get('gender')
            user.profile.save()
            messages.success(request, f'Your account has been created succesfully.')
            return redirect("login")

    else:
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileForm(request.POST)
    return render(request, 'user/register.html', {'u_form': u_form, 'p_form': p_form})


@login_required()
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated succesfully.')
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile.html', context)
