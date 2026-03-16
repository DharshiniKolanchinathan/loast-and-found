from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Profile is created by signal, just update it
            profile = user.profile
            profile.phone_number = form.cleaned_data['phone_number']
            profile.department = form.cleaned_data['department']
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        return render(request, 'accounts/register.html', {'form': form})

class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'user_form': user_form})

    @method_decorator(login_required)
    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'user_form': user_form})
