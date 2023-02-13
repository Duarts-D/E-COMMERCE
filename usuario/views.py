from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from usuario.forms import PerfilForm
from usuario.models import Perfil_Usuario

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
                return redirect('produto:produtos')

        return redirect('perfils:login')      
    def get(self, *args,**kwargs):
        return render(self.request,self.template_name)

class Cadastro(View):
    template_name = 'usuarios/cadastro.html'

    def setup(self, *args, **kwargs):
        super().setup( *args, **kwargs)
        
        self.contexto = {'perfilform':PerfilForm(data=self.request.POST or None)}
    
        self.perfilform = self.contexto['perfilform']


    def post(self,request, *args, **kwargs):

        nome = self.request.POST.get('nome')
        sobrenome  = self.request.POST.get('sobrenome')
        email = self.request.POST.get('email')
        cpf = self.request.POST.get('cpf')
        senha = self.request.POST.get('senha')
        
        user = User.objects.create_user(
            username=cpf,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome
        )
        user.save()
        
        if self.perfilform.is_valid():
            perfil = self.perfilform.save(commit=False)
            perfil.user = user
            perfil.save()

        return redirect('perfils:login')
    
    def get(self, *args,**kwargs):
        return render(self.request,self.template_name,self.contexto)
