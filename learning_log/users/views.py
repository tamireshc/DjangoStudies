from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


def logout_view(request):
    """Logout do usuário"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """Cadastro de usuário"""
    if request.method != "POST":
        form = UserCreationForm()
        form.fields["username"].label = "Usuário"
        form.fields["password1"].label = "Senha"
        form.fields["password2"].label = "Confirmação de Senha"

    else:
        # processa o formulário preenchido
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # Faz o login e redireciona para a pag index
            # print(request.POST)
            authenticate_user = authenticate(
                username=request.POST["username"], password=request.POST["password1"]
            )
            login(request, authenticate_user)
            return HttpResponseRedirect(reverse("index"))

    context = {"form": form}
    return render(request, "users/register.html", context)
