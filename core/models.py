from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nome_exibido = models.CharField(max_length=100)  # Ex: ~aluno:joao
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome_exibido} - {self.texto[:30]}'