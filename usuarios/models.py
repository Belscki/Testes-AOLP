from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    email = models.EmailField(max_length=254,null=True,blank=True)
    senha = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return self.nome