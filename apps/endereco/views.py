from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from apps.endereco.forms import Perfil_EndercoForm
from apps.endereco.models import Perfil_Endereco
from apps.usuario.models import Perfil_Usuario
from apps.utilidade.frete_correio import CalcularFreteCarrinho



class Endereco(View):
    template_name = 'endereco.html'
    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)

        self.contexto = {'perfil_endereco': Perfil_EndercoForm(data=self.request.POST or None)}
        self.perfil_form = self.contexto['perfil_endereco']

    def post(self,*args,**kwargs):
            
        if self.perfil_form.is_valid():
            cep = self.request.POST.get('cep')
            user = self.request.user
            perfils = get_object_or_404(Perfil_Usuario,user=user)

            perfil = self.perfil_form.save(commit=False)
            perfil.user_perfil = perfils
            perfil.save()
            

            if self.request.session.get('carrinho'):
                carrinho = self.request.session.get('carrinho')
                frete = CalcularFreteCarrinho(carrinho=carrinho,cep_destino=cep)
                frete = frete.calcular_frete_carrinho()

                self.request.session['frete'] = {'preco': frete[1]}
                self.request.session.save()     
                return redirect('pedido:pedido')
            else:
                return redirect('cars:carrinho')
        else:
            return render(self.request,self.template_name,self.contexto)
        
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:login')
        
        user = self.request.user
        perfils = Perfil_Usuario.objects.filter(user=user).first()
        perfil_endereco = Perfil_Endereco.objects.filter(user_perfil=perfils).exists()
        
        if perfils == None or '':
            return redirect('usuario:cadastro')

        if perfil_endereco:
           return redirect('pedido:pedido')

        return render(self.request,self.template_name,self.contexto)

class EnderecoAlterar(View):
    template_name = 'atualizar_endereco.html'

    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)
        self.perfil_usuario = Perfil_Usuario.objects.filter(user=self.request.user).first()
        self.perfil_endereco = Perfil_Endereco.objects.filter(user_perfil=self.perfil_usuario).first()
        self.contexto = {
            'perfil_endereco': Perfil_EndercoForm(
            data=self.request.POST or None,
            instance=self.perfil_endereco
            )
        }
        self.perfil_endereco = self.contexto['perfil_endereco']

    def post(self,*args,**kwargs):
        if self.perfil_endereco.is_valid():
            if self.request.user.is_authenticated:
                endereco = self.perfil_endereco.save(commit=False)
                endereco.user_perfil = self.perfil_usuario
                endereco.save()
                return redirect('pedido:pedido')

        return render(self.request,self.template_name,self.contexto)
   
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:login')
        
        return render(self.request,self.template_name,self.contexto)