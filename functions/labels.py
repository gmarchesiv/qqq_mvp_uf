


import math


def generar_label(params, vars):
    generar_garch(params, vars)





    pass



def generar_garch(params, vars):
    vars.varianza=params.omega+(params.alpha+params.gamma*vars.signo)*  math.pow(vars.retorno-params.mu, 2) +params.beta*vars.varianza
    vars.garch=round(100* math.sqrt(  params.days_year*vars.varianza),4)

 
    # TODO CALCULAR
    vars.retorno=0
    vars.signo=0

 