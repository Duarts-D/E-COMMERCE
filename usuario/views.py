from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from usuario.forms import PerfilForm
from usuario.models import Perfil_Usuario
from django.contrib import messages

class Login(View):
    template_name = 'usuarios/login.html'

    def post(self,*args,**kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email).values_list('username',flat=True).get()
            user = authenticate(self.request,
                username=username,password=password)

            if user is not None:
                login(self.request,user)

                
                if not self.request.session.get('carrinho'):
                    return redirect('produto:produtos')
                
                return redirect('cars:carrinho')
        
        messages.error(self.request,'Email ou senha incorreto')
        return redirect('usuario:login')      
    
    def get(self, *args,**kwargs):
        return render(self.request,self.template_name)

class Cadastro(View):
    template_name = 'usuarios/cadastro.html'

    def setup(self, *args, **kwargs):
        super().setup( *args, **kwargs)
        
        self.contexto = {'perfilform':PerfilForm(data=self.request.POST or None)}
    
        self.perfilform = self.contexto['perfilform']


    def post(self,request, *args, **kwargs):
        if self.perfilform.is_valid():
            nome = self.perfilform.cleaned_data.get('nome')
            sobrenome  = self.perfilform.cleaned_data.get('sobrenome')
            email = self.perfilform.cleaned_data.get('email')
            cpf = self.perfilform.cleaned_data.get('cpf')
            senha = self.perfilform.cleaned_data.get('senha')
            
        
            user = User.objects.create_user(
                username=cpf,
                email=email,
                password=senha,
                first_name=nome,
                last_name=sobrenome,
            )
            user.save()

            perfil = self.perfilform.save(commit=False)
            perfil.user = user
            perfil.save()

            return redirect('usuario:login')
        else:
            return render(self.request,self.template_name,self.contexto)
    
    def get(self, *args,**kwargs):
        return render(self.request,self.template_name,self.contexto)

class Logout(View):
    def get(self,*args,**kwargs):
        logout(self.request)
        messages.success(self.request,'Deslogado com sucesso')
        return redirect('produto:produtos')