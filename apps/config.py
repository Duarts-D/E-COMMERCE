from decouple import config,UndefinedValueError


SECRET_KEY = 'wxw#wsrei5e=2!385d4md$t+wk86xx2n@s)2ci*p+!m-#*hq#%' #Chave gerada aleatoria

try:
    CEPORIGEM = config('CEPORIGEM')
except UndefinedValueError:
    CEPORIGEM = '74215200'

try:
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_HOST= config('EMAIL_HOST')
except UndefinedValueError:
    print ('Favor preencher variaveis sensivel do email se necessario utilizar sistema de e-mail')


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')