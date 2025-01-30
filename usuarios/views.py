from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.messages import constants
from django.contrib import messages
from .utils import gerar_senha, analisar_senha
from django.contrib import auth

def cadastro(request):
    senha_sugerida = gerar_senha(10)

    if request.method == "GET":
        return render(request, 'cadastro.html', {'senha_sugerida': senha_sugerida})
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Armazenar as informações digitas na página de cadastro e devolver na tela se houver algum erro de incosistência
        request.session['form_data'] = request.POST
        form_data = request.session.get('form_data', {})
        #
        if not primeiro_nome :
            messages.add_message(request, constants.ERROR, 'Primeiro nome é obrigatório')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})

        if not ultimo_nome :
            messages.add_message(request, constants.ERROR, 'Último nome é obrigatório')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})

        if not username :
            messages.add_message(request, constants.ERROR, 'Userame é obrigatório')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})

        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Este usuário já está cadastrado')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        validacoes_senha = analisar_senha(senha, confirmar_senha)
        
        if not validacoes_senha['confirmar_senha']:
            messages.add_message(request, constants.ERROR, 'A senha e confirmar senha devem ser iguais')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['tamanho']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 8 dígitos')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['especial']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos um caracter especial')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['maiuscula']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos uma letra maiúscula')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['minuscula']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos uma letra minúscula')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        
        if not validacoes_senha['numeros']:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos um número')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
                
        if not email :
            messages.add_message(request, constants.ERROR, 'Email é obrigatório')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        elif '@' not in email :
            messages.add_message(request, constants.ERROR, 'Informe um email válido')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'Este email já está cadastrado')
            return render(request, 'cadastro.html', {'form_data': form_data, 'senha_sugerida': senha_sugerida})

        try:
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
            user.save()

            mensagem = f'Usuário {username} criado com sucesso!'
            messages.add_message(request, constants.SUCCESS, mensagem)
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Entrar em contato com o adminitrador')
            return redirect('/usuarios/cadastro')

        return redirect('/usuarios/login')    
    else:
        return HttpResponse('Método não suportado')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
			# Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/exames/solicitar_exames')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/usuarios/login')
    else: 
        messages.add_message(request, constants.ERROR, 'Método não suportado')
        return redirect('/usuarios/login')

def sair(request):
    auth.logout(request)
    return redirect('/usuarios/login')