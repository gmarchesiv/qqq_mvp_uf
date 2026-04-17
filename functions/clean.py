 


def clean_vars(vars):

    # LIMPIEZA DE vars
     
    vars.params_regla=""
    vars.compra = True
    vars.call=False
    vars.put=False

    vars.flag_real_priceBuy=False
 
    vars.minutos = 0
    vars.manifesto = False

    vars.ugs_n = 0
    vars.ugs_n_ant = 0
    vars.pico = 0
    vars.priceBuy = 0
    vars.price_Put_label=  0
    vars.d_Put_label=  0
    vars.price_Call_label= 0
    vars.d_Call_label=  0

    vars.rule = True
    vars.accion_mensaje = 0
    vars.bloqueo = True
    vars.status = "ON"
    vars.venta_intentos=0
    vars.tipo=""
    vars.real_priceBuy =0
    
    
    vars.flag_bloqueo_tiempo=False
    vars.flag_Call_R2 = False
    vars.flag_Put_R2 = False
    vars.flag_cambio_R1_label= False
    vars.flag_Call_label_1_compra=   False
    vars.flag_Call_label_2_compra= False

    vars.flag_Call_reset = {k: False for k in vars.flag_Call_reset}
    vars.flag_Put_reset = {k: False for k in vars.flag_Put_reset}

    vars.flag_cambio_fast= False

    vars.flag_Put_label_cambio= False
    vars.flag_bloqueo_put=False
    vars.flag_bloqueo_r1_e= False
    
    
    vars.flag_Call_label_cambio= False
    
     
    
 
 