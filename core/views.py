from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CadastroForm, ComentarioForm
from .models import Comentario
import random
from django.shortcuts import render, redirect
from .forms import CadastroForm, ComentarioForm
from django.utils.timezone import now

def home(request):
    return render(request, 'core/home.html')

def cadastro_view(request):
    form = CadastroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        grupo = Group.objects.get(name=form.cleaned_data['tipo'])
        user.groups.add(grupo)
        login(request, user)
        return redirect('sala')
    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def sala_view(request):
    comentarios = Comentario.objects.all().order_by('-criado_em')
    is_professor = request.user.groups.filter(name="Professor").exists()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            grupo = request.user.groups.first().name.lower() if request.user.groups.exists() else 'guest'
            comentario.nome_exibido = f"~{grupo}:{request.user.username}"
            comentario.criado_em = now()
            comentario.save()
            return redirect('sala')
    else:
        form = ComentarioForm()

    return render(request, 'core/sala.html', {
        'form': form,
        'comentarios': comentarios,
        'is_professor': is_professor,  # <- Aqui
    })
def guest_view(request):
    request.session['guest'] = True
    return redirect('sala')


def gerar_nome_visitante():
    return f"visitante{random.randint(1000, 9999)}"

def is_professor(user):
    return user.is_authenticated and user.groups.filter(name='Professor').exists()

@user_passes_test(is_professor)
def deletar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id)
    comentario.delete()
    return redirect('sala')

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        return redirect('sala')
    return render(request, 'core/login.html', {'form': form})
