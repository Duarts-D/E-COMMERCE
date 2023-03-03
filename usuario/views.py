from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from usuario.forms import PerfilForm,PasswordsForm,AlterarSenhaForm,SenhaEmailResetForm,SenhaResetConfirmForm
from usuario.models import Perfil_Usuario
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.urls import reverse_lazy
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
        
        self.contexto = {'perfilform':PerfilForm(data=self.request.POST or None),
                         'senhaforms':PasswordsForm(data=self.request.POST or None)}
    
        self.perfilform = self.contexto['perfilform']
        self.senhaforms = self.contexto['senhaforms']


    def post(self,request, *args, **kwargs):
        if self.perfilform.is_valid() and self.senhaforms.is_valid():
            nome = self.perfilform.cleaned_data.get('nome')
            sobrenome  = self.perfilform.cleaned_data.get('sobrenome')
            email = self.perfilform.cleaned_data.get('email')
            cpf = self.perfilform.cleaned_data.get('cpf')
            senha = self.senhaforms.cleaned_data.get('password')
            
            print(senha)
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

class AtualizarDadosgr(View):
    template_name = 'usuarios/atualizar_dados.html'


    def setup(self, request, *args, **kwargs,):
        super().setup(request, *args, **kwargs) 


        if self.request.user.is_authenticated:
            self.perfil = Perfil_Usuario.objects.filter(user=self.request.user).first()

            self.contexto = {'perfilform': PerfilForm(
                usuario=self.request.user,
                data=self.request.POST or None,
                instance=self.perfil),
                }
            
            self.perfilform = self.contexto['perfilform']

    def post(self,*args,**kwargs):
        if self.perfilform.is_valid():
            if self.request.user.is_authenticated:   

                user = get_object_or_404(User,username=self.request.user.username)
                user.username = self.perfilform.cleaned_data.get('cpf')
                user.first_name = self.perfilform.cleaned_data.get('nome')
                user.last_name = self.perfilform.cleaned_data.get('sobrenome')
                user.email = self.perfilform.cleaned_data.get('email')
                user.save()

                perfil = self.perfilform.save(commit=False)
                perfil.user = user
                perfil.save()
                print('atualizado')

                return redirect('usuario:atualizardados_gr')
        else:
            return render(self.request,self.template_name,self.contexto)

        


    def get(self,*args,**kwargs):
        return render(self.request,self.template_name,self.contexto)

class Logout(View):
    def get(self,*args,**kwargs):
        logout(self.request)
        messages.success(self.request,'Deslogado com sucesso')
        return redirect('produto:produtos')

class AtualizarSenhaview(PasswordChangeView):
    
    form_class = AlterarSenhaForm
    success_url = reverse_lazy('usuario:atualizacao_concluida')

def senha_sucesso(request):
    return render(request,'usuarios/senha_sucesso.html')

class RecuperarSenhaView(PasswordResetView):
    form_class = SenhaEmailResetForm
    email_template_name = 'usuarios/resetar_senha/senha_reset_email.html'
    success_url = reverse_lazy('usuario:recuperar_senha_enviado')

def recuperar_senha_enviado(request):
    return render(request,'usuarios/resetar_senha/senha_reset_enviada.html')

class RecuperarSenhaConfirmView(PasswordResetConfirmView):
    form_class = SenhaResetConfirmForm
    success_url = reverse_lazy('usuario:password_reset_complete')

pass  

# class ResetPasswordView(View):
#     template_name = 'usuarios/recuperar_senha.html'
#     def get(self,*args,**kwargs):
#         email = self.request.GET.get('email')
#         if email:
#             send_mail('RECUPERAÇAO DE SENHA',
#                       'Utilize esse link para reseta sua senha',
#                       '',[email],
#                       )
#             return redirect('usuario:login')
#         return render(self.request,self.template_name)