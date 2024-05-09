from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Usuario

from django.shortcuts import HttpResponse

def home(request):
    infos = {}
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')    
        usuario = Usuario.objects.get(id_usuario=user_id)
        infos = {'usuario':usuario}
        
    return render(request,'index.html', infos)

def cadastro(request):
    infos = {}
    if 'error_msg' in request.session:
        infos['error_msg'] = request.session.get('error_msg')
    
    return render(request,'cadastro.html', infos)

def login(request):
    infos = {}
    if 'error_msg' in request.session:
        infos['error_msg'] = request.session.get('error_msg')
    if 'email' in request.session:
        infos['email'] = request.session.get('email')
    
    return render(request,'login.html', infos)

def cadastrando(request):
    email = request.POST.get('email')
    if Usuario.objects.filter(email=email).first() is not None:
        request.session['error_msg'] = 'E-mail ja registrado'
        
        return redirect(reverse('cadastro'))
    else:
        novo_usuario = Usuario()
        novo_usuario.nome = request.POST.get('nome')
        novo_usuario.email = request.POST.get('email')
        novo_usuario.senha = make_password(request.POST.get('senha'))
        novo_usuario.save()
        
        email = request.POST.get('email')
        user = Usuario.objects.filter(email=email).first()

        request.session['user_id'] = user.id_usuario

        return redirect(reverse('home'))

def logando(request):
    email = request.POST.get('email')
    user = Usuario.objects.filter(email=email).first()
    if user is None:
        request.session['error_msg'] = 'Email Incorreto'
        request.session['email'] = email
        
        return redirect(reverse('login'))
    
    request_senha = request.POST.get('senha')
    user_senha = user.senha 

    if check_password(request_senha, user_senha):
        request.session['user_id'] = user.id_usuario
        
        return redirect(reverse('home'))    
    else:
        request.session['error_msg'] = 'Senha Incorreta!'
        request.session['email'] = email
        
        return redirect(reverse('login'))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        
    origem = request.GET.get('origem')
    if origem:
        return redirect(origem)
    else:
        return redirect(reverse('home'))
    
def del_vars(request):
    cache = {'email', 'error_msg'}
    for var in cache:
        if var in request.session:
            del request.session[var]
    return HttpResponse(status=200)