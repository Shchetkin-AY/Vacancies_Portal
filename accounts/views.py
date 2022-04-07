from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from vacancies.forms import RegisterUserForm, LoginUserForm


class RegisterUserView(View):
    def get(self, request):
        return render(request, "accounts/register.html", context={"form": RegisterUserForm})

    def post(self, request):
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data["password"])
            new_user.save()
            return redirect("login")
        else:
            register_form = RegisterUserForm()
            return render(request, "accounts/register.html", context={"register_form": register_form})


class LoginUserView(View):
    def get(self, request):
        return render(request, "accounts/login.html", context={"form": LoginUserForm})

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            new_user = form.cleaned_data
            user = authenticate(username=new_user['username'], password=new_user['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main')
                else:
                    raise HttpResponseNotFound
            else:
                raise HttpResponseNotFound
        else:
            form = LoginUserForm
            return render(request, 'accounts/login.html', context={'form': form})


class LogoutFormView(LogoutView):
    def logout(self, request):
        logout(request)
        return redirect('main')


class CustomHendler():
    def custom_handler404(request, exception):
        return HttpResponseNotFound('Ресурс или пользователь не найден!')

    def custom_handler500(request):
        return HttpResponseServerError('Ошибка сервера!')

