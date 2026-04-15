# ====================
#  - Librerias -
# ====================


import asyncio
from datetime import datetime
import time
 
from config.IB.options import buyOptionContract
from database.repository.repository import writeDayTrade

# from functions.broadcasting import broadcasting_buy, send_buy
from functions.broadcasting import send_buy
from functions.labels import generar_label
from functions.logs import printStamp, read_buy, readIBData_action
from functions.notifications import sendError
from functions.saveVars import saveVars


# INICIO DE LAS REGLAS DE COMPRA
def buyOptions(app,varsBc,varsLb,vars,params,params_call,params_put,debug_mode):

    #---------------------------------------------------
    '''
    En la compra de opciones, realizamos calculos y
    verificamos si esta en parametros de compra.
    '''
    #---------------------------------------------------
    
    calculos_previos(vars,varsLb, params,params_call,params_put,debug_mode)

    if vars.askbid_call < params.max_askbid_compra_abs and vars.cask > 0 and vars.promedio_call < params.max_askbid_compra_prom :
        calculos_call(vars, params,varsLb,params_call,debug_mode )
        buy_Call(app,varsBc,varsLb,vars,params,params_call,debug_mode)

    if vars.askbid_put < params.max_askbid_compra_abs and vars.pask > 0 and  vars.promedio_put < params.max_askbid_compra_prom and vars.compra==True:
        calculos_put(vars, params,params_put,debug_mode)
        buy_Put(app,varsBc,varsLb,vars,params,params_put,debug_mode)

    varsLb.label_ant=varsLb.label

def buy_Call(app,varsBc,varsLb,vars,params,params_call,debug_mode):
    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

    #---------------------------------------------------
    '''
    Reglas de compras de CALL.
    '''
    #---------------------------------------------------
 
    #########################################################
    ####################      CALL R2     ###################
    #########################################################

    if (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r2["TIME"][0] <= timeNow < params_call.r2["TIME"][1])
        and (params_call.r2["D"][0] <= vars.dcall < params_call.r2["D"][1])
        and (params_call.r2["DO"][0] <= vars.docall < params_call.r2["DO"][1])
        and (params_call.r2["DPUT"][0] <= vars.dput< params_call.r2["DPUT"][1]) and vars.askbid_put < params.max_askbid_compra_alt
        and  (varsLb.label==params_call.r2["LABEL"] )   
    ):
        vars.params_regla = params_call.r2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
    
    #########################################################
    ####################      CALL R2-2   ###################  
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r2_2["TIME"][0] <= timeNow < params_call.r2_2["TIME"][1])
        and (params_call.r2_2["D"][0] <= vars.dcall < params_call.r2_2["D"][1])
        and (params_call.r2_2["DO"][0] <= vars.docall < params_call.r2_2["DO"][1])
        and (params_call.r2_2["DPUT"][0] <= vars.dput< params_call.r2_2["DPUT"][1])and vars.askbid_put < params.max_askbid_compra_alt
        and   (varsLb.label==params_call.r2_2["LABEL"] )    
    ):
        vars.params_regla = params_call.r2_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
    #########################################################
    ####################      CALL R1     ################### COMENTAR
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r1["TIME"][0] <= timeNow < params_call.r1["TIME"][1])
        and (params_call.r1["D"][0] <= vars.dcall < params_call.r1["D"][1])
        and (params_call.r1["DO"][0] <= vars.docall < params_call.r1["DO"][1])
        and (params_call.r1["DPUT"][0] <= vars.dput< params_call.r1["DPUT"][1]) and vars.askbid_put < params.max_askbid_compra_alt
        and   (varsLb.label==params_call.r1["LABEL"] )    
        and vars.flag_Call_reset["R1"]
    ):
        vars.params_regla = params_call.r1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
    #########################################################
    ####################      CALL R1-2   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r1_2["TIME"][0] <= timeNow < params_call.r1_2["TIME"][1])
        and (params_call.r1_2["D"][0] <= vars.dcall < params_call.r1_2["D"][1])
        and (params_call.r1_2["DO"][0] <= vars.docall < params_call.r1_2["DO"][1])
        and (params_call.r1_2["DPUT"][0] <= vars.dput< params_call.r1_2["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and  (varsLb.label==params_call.r1_2["LABEL"] )     
    ):
        vars.params_regla = params_call.r1_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
    #########################################################
    ####################      CALL R1-3  ###################
    #########################################################
    elif (  
        (params_call.r1_3["TIME"][0] <= timeNow < params_call.r1_3["TIME"][1])
        and (params_call.r1_3["D"][0] <= vars.dcall < params_call.r1_3["D"][1])
        and (params_call.r1_3["DO"][0] <= vars.docall < params_call.r1_3["DO"][1])
        and (params_call.r1_3["DPUT"][0] <= vars.dput< params_call.r1_3["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.r1_3["LABEL"] )  
    ):
        vars.params_regla = params_call.r1_3
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ####################      CALL R1  E  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r1_e["TIME"][0] <= timeNow < params_call.r1_e["TIME"][1])
        and (params_call.r1_e["D"][0] <= vars.dcall < params_call.r1_e["D"][1])
        and (params_call.r1_e["DO"][0] <= vars.docall < params_call.r1_e["DO"][1])
        and (params_call.r1_e["DPUT"][0] <= vars.dput< params_call.r1_e["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.r1_e["LABEL"] )  
        and vars.flag_Call_reset["R1-E"]
        and not vars.flag_bloqueo_r1_e
    ):
        vars.params_regla = params_call.r1_e
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

 

    #########################################################
    ####################      CALL R1  I  ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
       (params_call.inv["TIME"][0] <= timeNow < params_call.inv["TIME"][1])
        and (params_call.inv["D"][0] <= vars.dcall < params_call.inv["D"][1])
        and (params_call.inv["DO"][0] <= vars.docall < params_call.inv["DO"][1])
        and (params_call.inv["DPUT"][0] <= vars.dput< params_call.inv["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        # and (varsLb.label==params_call.inv["LABEL"] ) 
    ):
        vars.params_regla = params_call.inv
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

 
    #########################################################
    ###################    CALL R1 FAST   ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
       (params_call.fast["TIME"][0] <= timeNow < params_call.fast["TIME"][1])
        and (params_call.fast["D"][0] <= vars.dcall < params_call.fast["D"][1])
        and (params_call.fast["DO"][0] <= vars.docall < params_call.fast["DO"][1])
        and (params_call.fast["DPUT"][0] <= vars.dput< params_call.fast["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.fast["LABEL"] ) 
        and vars.flag_cambio_fast 
        and vars.flag_Call_R2==False
    ):
        vars.params_regla = params_call.fast
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
  
    #########################################################
    ####################      CALL R3     ###################
    #########################################################

    elif (not (timeNow >= params.proteccion_compra_call_r1[0] and timeNow < params.proteccion_compra_call_r1[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.r3["TIME"][0] <= timeNow < params_call.r3["TIME"][1])
        and (params_call.r3["D"][0] <= vars.dcall < params_call.r3["D"][1])
        and (params_call.r3["DO"][0] <= vars.docall < params_call.r3["DO"][1])
        and (params_call.r3["DPUT"][0] <= vars.dput< params_call.r3["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.r3["LABEL"] )
        and vars.flag_Call_R2==False 
    ):
        vars.params_regla = params_call.r3
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
  
    #########################################################
    ####################      CALL R1  F  ################### COMENTAR
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
      (params_call.f1["TIME"][0] <= timeNow < params_call.f1["TIME"][1])
        and (params_call.f1["D"][0] <= vars.dcall < params_call.f1["D"][1])
        and (params_call.f1["DO"][0] <= vars.docall < params_call.f1["DO"][1])
        and (params_call.f1["DPUT"][0] <= vars.dput< params_call.f1["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.f1["LABEL"] )
     
    ):
        vars.params_regla = params_call.f1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
 

    #########################################################
    ####################      CALL R1  FAST2  ################## 
    #########################################################

    elif (not (timeNow >= params.proteccion_compra[0] and timeNow < params.proteccion_compra[1]) and 
                        not (timeNow >= params.proteccion_compra_2[0] and timeNow < params.proteccion_compra_2[1]) )and(
        (params_call.fast_2["TIME"][0] <= timeNow < params_call.fast_2["TIME"][1])
        and (params_call.fast_2["D"][0] <= vars.dcall < params_call.fast_2["D"][1])
        and (params_call.fast_2["DO"][0] <= vars.docall < params_call.fast_2["DO"][1])
        and (params_call.fast_2["DPUT"][0] <= vars.dput< params_call.fast_2["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.fast_2["LABEL"] )
          and  vars.flag_Call_reset["FAST_2"]
    ):
        vars.params_regla = params_call.fast_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
 
 
    
    #########################################################
    ####################      CALL LABEL 1     ###################
    #########################################################

    elif ( 
       (params_call.label_1["TIME"][0] <= timeNow < params_call.label_1["TIME"][1])
        and (params_call.label_1["D"][0] <= vars.dcall < params_call.label_1["D"][1])
        and (params_call.label_1["DO"][0] <= vars.docall < params_call.label_1["DO"][1])
        and (params_call.label_1["DPUT"][0] <= vars.dput< params_call.label_1["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.label_1["LABEL"] )
    ):
       vars.flag_Call_label_1_compra=True
  

  #########################################################
    ####################      CALL LABEL 2     ###################
    #########################################################

    elif ( 
       (params_call.label_2["TIME"][0] <= timeNow < params_call.label_2["TIME"][1])
        and (params_call.label_2["D"][0] <= vars.dcall < params_call.label_2["D"][1])
        and (params_call.label_2["DO"][0] <= vars.docall < params_call.label_2["DO"][1])
        and (params_call.label_2["DPUT"][0] <= vars.dput< params_call.label_2["DPUT"][1])  and vars.askbid_put < params.max_askbid_compra_alt
        and (varsLb.label==params_call.label_2["LABEL"] )
    ):
        vars.flag_Call_label_2_compra=True

    #########################################################
    ####################      CALL R1-LABEL   ############### 
    #########################################################
    if ( (params_call.label_1["TIME"][0]  <= timeNow< params_call.label_1["TIME-FIN"]) 
        and vars.flag_Call_label_1_compra 
        and (params_call.label_1["UMBRAL_COMPRA"][0] <= vars.d_Call_label <= params_call.label_1["UMBRAL_COMPRA"][1])
        
    ):
        vars.params_regla = params_call.label_1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
        
    #########################################################
    ####################      CALL R1-LABEL 2  ############### 
    #########################################################
    if ((params_call.label_2["TIME"][0]  <= timeNow< params_call.label_2["TIME-FIN"])  
        and vars.flag_Call_label_2_compra 
        and  (params_call.label_2["UMBRAL_COMPRA"][0] <= vars.d_Call_label <= params_call.label_2["UMBRAL_COMPRA"][1])
        
    ):
        vars.params_regla = params_call.label_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "C",vars.params_regla["REGLA"]  ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
            
def buy_Put(app,varsBc,varsLb,vars,params,params_put,debug_mode):
    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()
    #---------------------------------------------------
    '''
    Reglas de compras de PUT.
    '''
    #---------------------------------------------------
    
    #########################################################
    ####################       PUT R2     ###################
    #########################################################
    if ( 
        not(
              vars.askbid_put> params.max_askbid_compra_abs   and
           ( (  params.proteccion_compra_r2[0]<= timeNow < params.proteccion_compra_r2[1]) or 
            (  params.proteccion_compra_2[0]<= timeNow < params.proteccion_compra_2[1]) )
        )and
 
        (params_put.r2["TIME"][0] <= timeNow< params_put.r2["TIME"][1])
        and (params_put.r2["D"][0] <= vars.dput < params_put.r2["D"][1])
        and  (params_put.r2["DO"][0] <=  vars.doput < params_put.r2["DO"][1])
        and  (params_put.r2["DCALL"][0] <= vars.dcall < params_put.r2["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.r2["LABEL"] )
          and vars.flag_Put_reset["R2"]
          and not vars.flag_bloqueo_put

    ):
        vars.params_regla = params_put.r2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
 
    #########################################################
    ####################       PUT R2   E ###################
    #########################################################
    elif ( 
        (params_put.r2_e["TIME"][0] <= timeNow< params_put.r2_e["TIME"][1])
        and (params_put.r2_e["D"][0] <= vars.dput < params_put.r2_e["D"][1])
        and  (params_put.r2_e["DO"][0] <=  vars.doput < params_put.r2_e["DO"][1])
        and (varsLb.label==params_put.r2_e["LABEL"] )
        and vars.flag_Put_reset["R2-E"]  
        and not vars.flag_bloqueo_put

    ):
        vars.params_regla = params_put.r2_e
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
 
    #########################################################
    ###################    PUT R2 FAST    ###################
    #########################################################
    elif ( 
        (params_put.r2_fast["TIME"][0] <= timeNow< params_put.r2_fast["TIME"][1])
        and (params_put.r2_fast["D"][0] <= vars.dput < params_put.r2_fast["D"][1])
        and  (params_put.r2_fast["DO"][0] <=  vars.doput < params_put.r2_fast["DO"][1])
        and  (params_put.r2_fast["DCALL"][0] <= vars.dcall < params_put.r2_fast["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.r2_fast["LABEL"] )
          and vars.flag_Put_reset["R2-FAST"]

    ):
        vars.params_regla = params_put.r2_fast
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
    
    #########################################################
    ####################       PUT R3     ###################
    #########################################################
    elif ( 
        (params_put.r3["TIME"][0] <= timeNow< params_put.r3["TIME"][1])
        and (params_put.r3["D"][0] <= vars.dput < params_put.r3["D"][1])
        and  (params_put.r3["DO"][0] <=  vars.doput < params_put.r3["DO"][1])
        and  (params_put.r3["DCALL"][0] <= vars.dcall < params_put.r3["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.r3["LABEL"] )
        and vars.flag_Put_reset["R3"]
    ):
        vars.params_regla = params_put.r3
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ###################    PUT R1 FAST    ###################
    #########################################################
    elif ( 
        (params_put.fast["TIME"][0] <= timeNow< params_put.fast["TIME"][1])
        and (params_put.fast["D"][0] <= vars.dput < params_put.fast["D"][1])
        and  (params_put.fast["DO"][0] <=  vars.doput < params_put.fast["DO"][1])
        and  (params_put.fast["DCALL"][0] <= vars.dcall < params_put.fast["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.fast["LABEL"] )
          and  vars.flag_Put_reset["FAST"]

    ):
        vars.params_regla = params_put.fast
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ###################    PUT R1 LABEL    ###################
    #########################################################
    elif ( 
        (params_put.label_1["TIME"][0] <= timeNow< params_put.label_1["TIME"][1])
        and (params_put.label_1["D"][0] <= vars.dput < params_put.label_1["D"][1])
        and  (params_put.label_1["DO"][0] <=  vars.doput < params_put.label_1["DO"][1])
        and  (params_put.label_1["DCALL"][0] <= vars.dcall < params_put.label_1["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.label_1["LABEL"] )
        and vars.flag_Put_reset_esc["LABEL-1"]
        and vars.flag_cambio_R1_label

    ):
        vars.params_regla = params_put.label_1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""


    #########################################################
    ###################    PUT R1 LABEL 2  ###################
    #########################################################
    elif ( 
        (params_put.label_2["TIME"][0] <= timeNow< params_put.label_2["TIME"][1])
        and (params_put.label_2["D"][0] <= vars.dput < params_put.label_2["D"][1])
        and  (params_put.label_2["DO"][0] <=  vars.doput < params_put.label_2["DO"][1])
        and  (params_put.label_2["DCALL"][0] <= vars.dcall < params_put.label_2["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.label_2["LABEL"] )
        and vars.flag_Put_reset_esc["LABEL-2"] 
        and vars.flag_cambio_R1_label

    ):
        vars.params_regla = params_put.label_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ####################       PUT R1 I2   ################## 
    #########################################################
    elif ( 
        (params_put.inv_2["TIME"][0] <= timeNow< params_put.inv_2["TIME"][1])
        and (params_put.inv_2["D"][0] <= vars.dput < params_put.inv_2["D"][1])
        and  (params_put.inv_2["DO"][0] <=  vars.doput < params_put.inv_2["DO"][1])
        and  (params_put.inv_2["DCALL"][0] <= vars.dcall < params_put.inv_2["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.inv_2["LABEL"] )
    ):
        vars.params_regla = params_put.inv_2
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
 
    #########################################################
    ####################       PUT R1 I3   ###################
    #########################################################
    elif ( 
        (params_put.inv_3["TIME"][0] <= timeNow< params_put.inv_3["TIME"][1])
        and (params_put.inv_3["D"][0] <= vars.dput < params_put.inv_3["D"][1])
        and  (params_put.inv_3["DO"][0] <=  vars.doput < params_put.inv_3["DO"][1])
        and  (params_put.inv_3["DCALL"][0] <= vars.dcall < params_put.inv_3["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.inv_3["LABEL"] )

    ):
        vars.params_regla = params_put.inv_3
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ####################       PUT R1 I4   ################### COMENTADA
    #########################################################
    elif ( 
        (params_put.inv_4["TIME"][0] <= timeNow< params_put.inv_4["TIME"][1])
        and (params_put.inv_4["D"][0] <= vars.dput < params_put.inv_4["D"][1])
        and  (params_put.inv_4["DO"][0] <=  vars.doput < params_put.inv_4["DO"][1])
        and  (params_put.inv_4["DCALL"][0] <= vars.dcall < params_put.inv_4["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.inv_4["LABEL"] )

    ):
        vars.params_regla = params_put.inv_4
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #########################################################
    ####################       PUT R1 I5   ################### COMENTADA
    #########################################################
    elif ( 
        (params_put.inv_5["TIME"][0] <= timeNow< params_put.inv_5["TIME"][1])
        and (params_put.inv_5["D"][0] <= vars.dput < params_put.inv_5["D"][1])
        and  (params_put.inv_5["DO"][0] <=  vars.doput < params_put.inv_5["DO"][1])
        and  (params_put.inv_5["DCALL"][0] <= vars.dcall < params_put.inv_5["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.inv_5["LABEL"] )

    ):
        
        vars.params_regla = params_put.inv_5
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""
       
 
 
    
    ########################################################
    ###################       PUT R1 F   ################### COMENTAR
    ########################################################
    elif ( 
        (params_put.f1["TIME"][0] <= timeNow< params_put.f1["TIME"][1])
        and (params_put.f1["D"][0] <= vars.dput < params_put.f1["D"][1])
        and  (params_put.f1["DO"][0] <=  vars.doput < params_put.f1["DO"][1])
        and  (params_put.f1["DCALL"][0] <= vars.dcall < params_put.f1["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        

    ):
        vars.params_regla = params_put.f1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    ########################################################
    ###################       PUT R1 F INV_1  ################### COMENTAR
    ########################################################
    elif ( 
      (params_put.f_inv_1["TIME"][0] <= timeNow< params_put.f_inv_1["TIME"][1])
        and (params_put.f_inv_1["D"][0] <= vars.dput < params_put.f_inv_1["D"][1])
        and  (params_put.f_inv_1["DO"][0] <=  vars.doput < params_put.f_inv_1["DO"][1])
        and  (params_put.f_inv_1["DCALL"][0] <= vars.dcall < params_put.f_inv_1["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.f_inv_1["LABEL"] )
 
    ):
        vars.params_regla = params_put.f_inv_1
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

    #######################################################
    ##################       PUT R1 F INV_3  ################### COMENTAR
    #######################################################
    elif ( 
      (params_put.f_inv_3["TIME"][0] <= timeNow< params_put.f_inv_3["TIME"][1])
        and (params_put.f_inv_3["D"][0] <= vars.dput < params_put.f_inv_3["D"][1])
        and  (params_put.f_inv_3["DO"][0] <=  vars.doput < params_put.f_inv_3["DO"][1])
        and  (params_put.f_inv_3["DCALL"][0] <= vars.dcall < params_put.f_inv_3["DCALL"][1])  and vars.askbid_call < params.max_askbid_compra_alt
        and (varsLb.label==params_put.f_inv_3["LABEL"] )
 
    ):
        vars.params_regla = params_put.f_inv_3
        trade=buy(
            app,varsBc,varsLb,vars,params,
            "P",  vars.params_regla["REGLA"] ,debug_mode
        )
        if not trade:
            vars.params_regla = ""

   
 
    
     
def buy(app,varsBc,varsLb,vars,params, tipo, regla ,debug_mode):

    from rules.routine import calculations

    #---------------------------------------------------
    '''
    Compra de la opcion, La rutina consta de lo siguiente:
 
        1) Realiza Broadcasting de compra.
        2) Verifica que la compra se pueda dar sin 
           problemas de ASKBID.
        3) Ejecuta la orden de compra.
        4)Espera que la transaccion se complete,mientras
          sigue calculando variables.
        5) Al finalizar modifica variables de estado de 
           compra.
    '''
    #---------------------------------------------------
    if debug_mode:
        # SET DE VARIABLES
        vars.compra = False
        vars.minutos = 0
        vars.n_minutos = 0
        vars.minutos_trade = 0
        if tipo == "C":
            vars.tipo = regla
            vars.call = True
            vars.regla = f"CALL - {regla}"
            vars.regla_ant = vars.regla
            vars.status = "CALL"
            vars.priceBuy=vars.cask
        elif tipo == "P":
            vars.tipo = regla
            vars.put = True
            vars.regla = f"PUT - {regla}"
            vars.regla_ant = vars.regla
            vars.status = "PUT"
            vars.priceBuy=vars.pask
        else:
            return False
        
        vars.df.loc[vars.i, "REGLA"]=vars.status
        vars.df.loc[vars.i, "TIPO"]=vars.tipo
        print(vars.df["FECHA"][vars.i],vars.status,vars.tipo)
        return True



    else:

        if tipo =="C":
            ask=vars.cask
            contract=app.options[1]["contract"]
            symbol=app.options[1]["symbol"]
        else:
            ask=vars.pask
            contract=app.options[2]["contract"]
            symbol=app.options[2]["symbol"]

        
        #BROADCASTING
        if varsBc.buy ==False:
            asyncio.run(send_buy(app, varsBc, params, tipo,regla))
        # LECTURA PREVIA
        readIBData_action(app, vars, tipo, regla)

        # ENVIO DE ORDEN DE COMPRA
        flag = buyOptionContract(app, params, vars, ask, tipo, contract, symbol)
        if flag == False:
            printStamp("-NO SE PUDO CONCRETAR LA COMPRA-")
            return False

        # ESPERA DE LA ORDEN DE COMPRA
        app.statusIB = False
        app.Error = False

        printStamp("-wait Status-")
        vars.regla = f"BUY"

        while app.statusIB == False:

            timeNow = datetime.now(params.zone).time()

            if (timeNow.minute % 10 == 0 or timeNow.minute % 10 == 5):
                if varsLb.flag_minuto_label:
                    generar_label(params, varsLb,app)
                    varsLb.flag_minuto_label=False
                    time.sleep(0.5)
            else:
                varsLb.flag_minuto_label=True

            # if int(timeNow.second) in params.frecuencia_accion:
            calculations(app, vars,varsBc, params) 
            # ESPERANDO Y REGISTRANDO
            vars.status = "BUYING"
            saveVars(vars, app, params, False)
            writeDayTrade(app, vars,varsLb, params)
            vars.regla = f""  
                
            if app.Error:
                break
            time.sleep(0.5)
        if app.Error:
            printStamp(f"-COMPRA NO PROCESADA-")
            sendError(params, "COMPRA NO PROCESADA")
            return False

        # SET DE VARIABLES
        vars.compra = False
        vars.minutos = 0
        vars.n_minutos = 0
        vars.minutos_trade = 0
        if tipo == "C":
            vars.tipo = regla
            vars.call = True
            vars.regla = f"CALL - {regla}"
            vars.regla_ant = vars.regla
            vars.status = "CALL"
        elif tipo == "P":
            vars.tipo = regla
            vars.put = True
            vars.regla = f"PUT - {regla}"
            vars.regla_ant = vars.regla
            vars.status = "PUT"
        else:
            return False
        read_buy(vars)
        return True

def calculos_call(vars, params,varsLb,params_call,debug_mode):
    from datetime import time as dt_time

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()
    #---------------------------------------------------
    '''
    Calculos de call para bloquear o habilitar reglas 
    de compra.
    '''
    #---------------------------------------------------


    if vars.flag_Call_label_cambio and vars.price_Call_label==0:
        vars.price_Call_label =vars.cbid
    if vars.price_Call_label!=0:
        vars.d_Call_label= (vars.cbid/vars.price_Call_label)-1

    #########################################################
    ###################      CALCULOS      ##################
    #########################################################
 

    
    # RESET BASICO
    for variable,parametro in params_call.__dict__.items():
        regla=parametro["REGLA"]
        if regla in vars.flag_Call_reset:

            if vars.docall>= parametro["DO"][1]:
                vars.flag_Call_reset[regla] = False
            elif vars.docall< parametro["DO"][0]:
                vars.flag_Call_reset[regla] = True
            else:continue


    
    if debug_mode and vars.i>0:

        if (vars.flag_cambio_fast==False  and  
            varsLb.label==params_call.fast["LABEL"]   and 
            vars.df["FECHA"][vars.i]==vars.df["FECHA"][vars.i-1] and  #EVITA EL CAMBIO DE NOCHE A MAñana
            varsLb.label!=varsLb.label_ant):

            vars.flag_cambio_fast=True
    else:
        if (vars.flag_cambio_fast==False  and  
            varsLb.label==params_call.fast["LABEL"]   and  
        timeNow >= dt_time(9, 33) and  #EVITA EL CAMBIO DE NOCHE A MAñana
        varsLb.label!=varsLb.label_ant):

            vars.flag_cambio_fast=True
  

def calculos_put(vars, params,params_put,debug_mode ):

    #########################################################
    ###################      CALCULOS      ##################
    #########################################################

    
    if vars.flag_Put_label_cambio and vars.price_Put_label==0:
        vars.price_Put_label =vars.pbid
    if vars.price_Put_label!=0:
        vars.d_Put_label= (vars.pbid/vars.price_Put_label)-1


    diff=vars.dcall+vars.dput
    if ((diff<=params.limite_Put_bloqueo[0] or diff>=params.limite_Put_bloqueo[1])
                    and ( vars.askbid_call < params.max_askbid_compra_abs and vars.cask > 0 and vars.promedio_call < params.max_askbid_compra_prom )):
                    

        vars.flag_bloqueo_put=True


    # RESET BASICO
    for variable,parametro in params_put.__dict__.items():
        regla=parametro["REGLA"]
        if regla in vars.flag_Put_reset:
            if vars.doput >= parametro["DO"] [1]:
                vars.flag_Put_reset[regla] = False
            elif vars.doput < parametro["DO"] [0]:
                vars.flag_Put_reset[regla] = True
            else:continue

    if debug_mode and vars.i>0:
        vars.doput_ant = vars.df["DOPUT"][vars.i-1]   
    
    for variable,parametro in params_put.__dict__.items():
        regla=parametro["REGLA"]
        if regla in vars.flag_Put_reset_esc:

            if vars.doput>= parametro["DO"] [1]:
                vars.flag_Put_reset_esc[regla] = False

            elif  vars.flag_Put_reset_esc[regla] == False and\
            vars.doput_ant < vars.doput and \
                ( parametro["DO"] [0] <= vars.doput<= parametro["DO"] [1]):
                vars.flag_Put_reset_esc[regla] = True
                
            elif vars.doput< parametro["DO"] [0]:
                vars.flag_Put_reset_esc[regla] = True
            else:
                pass



    if debug_mode and vars.i>0:
        pass
    else:
        vars.doput_ant = vars.doput  


def calculos_previos(vars,varsLb, params,params_call,params_put,debug_mode):

    from datetime import time as dt_time

    if debug_mode:
        timeNow=vars.df["HORA"][vars.i]
    else:
        timeNow = datetime.now(params.zone).time()

    # PROMEDIOS DE ASKBID
    vars.promedio_call  = sum(vars.askbid_call_prom) / len(vars.askbid_call_prom) if len(vars.askbid_call_prom)!=0 else 0
    vars.promedio_put  = sum(vars.askbid_put_prom) / len(vars.askbid_put_prom) if len(vars.askbid_put_prom)!=0 else 0
 

    if (timeNow < params_call.r1_e["BLOQUEO_TIME"] and (vars.docall>params_call.r1_e["BLOQUEO_DOCALL"]  or
        vars.doput>params_call.r1_e["BLOQUEO_DOPUT"]  
        )):

        vars.flag_bloqueo_r1_e=True
  
 
    if debug_mode and vars.i>0:
   

        if  (( timeNow <=  params_put.label_2 ["TIME"][1] ) and 
            ( varsLb.label!=varsLb.label_ant  and
                varsLb.label==params_put.label_2 ["LABEL"] and 
                vars.flag_cambio_R1_label==False)and
                vars.df["FECHA"][vars.i]==vars.df["FECHA"][vars.i-1]  #EVITA EL CAMBIO DE NOCHE A MAñana
                ) :
            vars.flag_cambio_R1_label=True
        

    else:
 

        if  (( timeNow <=  params_put.label_2 ["TIME"][1] ) and 
            ( varsLb.label!=varsLb.label_ant  and
                varsLb.label==params_put.label_2 ["LABEL"] and 
                vars.flag_cambio_R1_label==False)and
                timeNow >= dt_time(9, 33)    #EVITA EL CAMBIO DE NOCHE A MAñana
                ) :
            vars.flag_cambio_R1_label=True

 
    if  (varsLb.label!=varsLb.label_ant and  varsLb.label ==0
        and ((params_call.label_1["TIME"][0]  <= timeNow  < params_call.label_1["TIME"][1])
            or  (params_call.label_2["TIME"][0] <= timeNow  <params_call.label_2["TIME"][1]))
        ):  
        vars.flag_Call_label_cambio=True
        vars.minutos =0
    
    else:
        if varsLb.label!=0 or  vars.minutos >=5:
            vars.flag_Call_label_cambio=False
            vars.price_Call_label=0
            vars.d_Call_label=0
            vars.flag_Call_label_1_compra=False
            vars.flag_Call_label_2_compra=False 

 