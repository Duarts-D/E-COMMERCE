from django.shortcuts import render,redirect
from django.views import View
from endereco.models import Perfil_Endereco
from usuario.models import Perfil_Usuario

class Pagamento(View):
    template_name ='pagamentos/pagamento.html'
    
    def setup(self,request,*args,**kwargs):
        super().setup(request,*args,**kwargs)


        user = Perfil_Usuario.objects.get(user=self.request.user)
        perfil_user = Perfil_Endereco.objects.get(user_perfil=user.id)
        
        
        self.contexto = {
            'perfil_usuario': perfil_user, 
        }

    def get(self,*args,**kwargs):
        user = Perfil_Usuario.objects.filter(user=self.request.user).first()
        perfil_user = Perfil_Endereco.objects.filter(user_perfil=user.id).exists()
        
        print(perfil_user)

        if user is None or perfil_user is None :
            return redirect('usuario:login')
        
        return render(self.request,self.template_name,self.contexto)