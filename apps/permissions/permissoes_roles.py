from rolepermissions.roles import AbstractUserRole

class Funcionario_estoque(AbstractUserRole):
    # Responsavel pela separaçao do material
    available_permissions = {'gerar_pdf': True}

class Funcionario_baixar(AbstractUserRole):
    # Responsavel pela alteraçao do status do pedido apos receber o pdf preenchido 
    # pelo funcionario do estoque
    available_permissions = {'alterar_status':True,'gerar_pdf': True}

class Gerente_estoque(AbstractUserRole):
    # Gerente responsavel para subir quantidade de estoque pro site
    available_permissions = {'alimentar_estoque':True,'alterar_status':True,'gerar_pdf': True}