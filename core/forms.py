from django import forms
from django.contrib.auth.models import User
from .models import Comentario

class CadastroForm(forms.ModelForm):
    TIPO_USUARIO = [('Aluno', 'Aluno'), ('Professor', 'Professor')]

    tipo = forms.ChoiceField(choices=TIPO_USUARIO, label='Classe')
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha')

    class Meta:
        model = User
        fields = ['username', 'password', 'tipo']
        labels = {
            'username': 'Nome',
        }

class ComentarioForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), label='Escreva seu comentário')

    class Meta:
        model = Comentario
        fields = ['texto']