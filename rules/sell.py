# ====================
#  - Librerias -
# ====================
import asyncio
from datetime import datetime
import time


from config.IB.options import sellOptionContract
from database.repository.repository import writeDayTrade

from functions.broadcasting import comparar_precios, send_sell, verificar_regla
from functions.logs import printStamp, read_rentabilidad, read_sell, readIBData_action
from functions.notifications import sendError
from functions.saveJson import saveJson

# ====================
#  - Funciones -
# ====================


# INICIO DE LAS REGLAS DE VENTA
def sellOptions(app, vars, params):
    if vars.minutos_trade <=params.tiempo_contulta and vars.venta_intentos >=params.intentos:

        asyncio.run(comparar_precios(vars, params))
    vars.venta_intentos+=1
    if vars.call:
        sellCall(app, params, vars)
        return
    elif vars.put:
        sellPut(app, params, vars)
        return
    else:
        return


def sell_obligatoria(app, vars, params,tipo):
    params.max_askbid_venta=params.max_askbid_venta_forzada
    if tipo == "C":
        val = 1
        if vars.askbid_call > params.max_askbid_venta or vars.cbid <= 0:
            return False
    elif tipo == "P":
        val = 2
        if vars.askbid_put > params.max_askbid_venta or vars.pbid <= 0:
            return False
    else:
        print("-ERROR SELL OBLIGATORIO-")
        return
    vars.venta_intentos=params.intentos
    sell(
            app,
            vars,
            params,
           tipo,
            "FORZADO",
            app.options[val]["contract"],
            app.options[val]["symbol"],
        )
    return


def sellCall(app, params, vars):

    timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_call > params.max_askbid_venta:
        vars.rentabilidad = vars.cbid / vars.priceBuy - 1
        read_rentabilidad(vars)
        return
    if vars.cbid <= 0:
        return
    vars.rentabilidad = vars.cbid / vars.priceBuy - 1

    read_rentabilidad(vars)

    # CALCULAR RENTABILIDAD vars.pico
    if vars.pico < vars.rentabilidad:
        vars.pico = vars.rentabilidad

    vars.caida = vars.rentabilidad - vars.pico

    # FIN DE DIA DE TRADE
    # if timeNow >= params.fd and   vars.tipo == "U":
    #     vars.venta_intentos=params.intentos
    #     name = "FD-U"
         
        
    #     sell(
    #         app,
    #         vars,
    #         params,
    #         "C",
    #         name,
    #         app.options[1]["contract"],
    #         app.options[1]["symbol"],
    #     )
    #     return
    
    if timeNow >= params.fd:
        vars.venta_intentos=params.intentos
      
        name = "FD"
        sell(
            app,
            vars,
            params,
            "C",
            name,
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )
        return

    # REGLA DE PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_c
        and vars.rentabilidad < (vars.pico - params.perdida_maxima_c)
        and vars.manifesto == False
    ):
        sell(
            app,
            vars,
            params,
            "C",
            "PROTECCION",
            app.options[1]["contract"],
            app.options[1]["symbol"],
        )

        return

    #########################################################
    ################      CALL  R1    ##################
    #########################################################
    if vars.tipo == "R1" or vars.tipo == "R1-E":

        if (
            (
                vars.dcall > params.umbral_manifestacion_cu
                or vars.docall > params.umbral_manifestacion_cu
            )
            and vars.flag_umbral_cr1 == False
            and timeNow < params.timeCall_umbral
        ):
            vars.flag_umbral_cr1 = True
            vars.ugs_n = 0

            vars.manifesto = True
            vars.tipo = "U"

        if vars.flag_umbral_cr1 == False:

            # MANIFIESTA

            if vars.manifesto:

                # DIAMANTE

                for y in range(vars.ugs_n, len(params.diamante_cr1)):
                    if round(vars.pico, 3) > params.diamante_cr1[y]:
                        vars.ugs_n = y
                        if vars.ugs_n != vars.ugs_n_ant:
                            vars.minutos = 0
                            vars.ugs_n_ant = vars.ugs_n
                    else:
                        break

                # MAXIMA RENTABILIDAD

                if vars.rentabilidad <= (vars.pico - params.resta_cr1[vars.ugs_n]):

                    name = f"T{vars.ugs_n}"
                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        name,
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

                else:
                    pass

            # AUN NO MANIFIESTA
            else:

                # TOMA DE DESICION

                if (
                    vars.minutos >= params.min_desicion_cr1
                    and (vars.flag_pos == False or vars.flag_neg == False)
                    and vars.flag_desicion
                ):

                    if vars.rentabilidad >= 0:
                        vars.flag_pos = True
                        vars.min_extras = params.min_extras_pos
                    else:
                        vars.flag_neg = True
                        vars.min_extras = params.min_extras_neg
                    vars.flag_desicion = False

     
                # ------------------------------
                # vars.manifesto
                if vars.rentabilidad >= params.umbral_manifestacion_cR1:
                    vars.manifesto = True
                    vars.minutos = 0

                # NO SE vars.manifesto POR TIEMPO POSITIVO
                elif vars.minutos >= (params.min_desicion_cr1 + vars.min_extras) and (
                    vars.flag_pos and vars.flag_neg == False
                ):

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "NMT-P",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

                # NO SE vars.manifesto POR TIEMPO REBPOTE
                elif vars.minutos >= (vars.min_extras) and (
                    vars.flag_pos and vars.flag_neg
                ):

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "NMT-P",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

                # NO SE vars.manifesto POR TIEMPO
                elif vars.minutos >= (params.min_desicion_cr1 + vars.min_extras) and (
                    vars.flag_neg and vars.flag_pos == False
                ):

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "NMT-N",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

                # STOP LOSS ANTES DE DESICION
                elif vars.rentabilidad <= params.sl_cr1 and vars.flag_desicion:

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "SL",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

                # DESICION POSITIVA
                elif vars.flag_pos:

                    # SL - POSITIVO

                    if vars.rentabilidad <= params.sl_cr1_p and vars.flag_neg == False:

                        sell(
                            app,
                            vars,
                            params,
                            "C",
                            "NMR-P",
                            app.options[1]["contract"],
                            app.options[1]["symbol"],
                        )

                        return

                    if vars.rentabilidad <= params.sl_cr1_rebote and vars.flag_neg:

                        sell(
                            app,
                            vars,
                            params,
                            "C",
                            "NMR-P",
                            app.options[1]["contract"],
                            app.options[1]["symbol"],
                        )

                        return

                # DESICION NEGATIVA

                elif vars.flag_neg and vars.flag_pos == False:

                    # REBOTA
                    if vars.rentabilidad >= 0:

                        vars.min_extras = params.min_extras_rebote
                        vars.minutos = 0

                        # flag_neg = False
                        vars.flag_pos = True

                    # SL - NEGATIVO
                    elif vars.rentabilidad <= params.sl_cr1_n:

                        sell(
                            app,
                            vars,
                            params,
                            "C",
                            "NMR-N",
                            app.options[1]["contract"],
                            app.options[1]["symbol"],
                        )

                        return

                else:
                    pass

    #########################################################
    ################      CALL    R2    ##################
    #########################################################
    elif vars.tipo == "R2":

        # MANIFIESTA
        if vars.manifesto:
            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_cr2)):
                if round(vars.pico, 3) > params.diamante_cr2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break
            # MAXIMA RENTABILIDAD
            if vars.rentabilidad <= (vars.pico - params.resta_cr2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    name,
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_cR2:
                vars.manifesto = True
                vars.minutos = 0

            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr2:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

    #########################################################
        ####################      CALL  R1 -C  ###################
        #########################################################

    elif vars.tipo == "R1-C":
        
        


        if vars.manifesto:
                

            if vars.pico>=params.target_r1_c and vars.rentabilidad <= (vars.pico-params.resta_r1_c):

                sell(
                app,
                vars,
                params,
                "C",
                "TARGET",
                app.options[1]["contract"],
                app.options[1]["symbol"],
            )

                return

            # NMT
            elif vars.minutos>= (params.min_desicion_cr1_c ):
                sell(
                app,
                vars,
                params,
                "C",
                "NMT",
                app.options[1]["contract"],
                app.options[1]["symbol"],
            )

                return

            # NMT
            elif vars.rentabilidad <=params.retroceso_abs_cr1_c:
                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "NMR",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return


        else:
            # MANIFESTO
            if vars.rentabilidad >= params.umbral_manifestacion_cr1_c:
                vars.manifesto = True
                vars.minutos = 0

            # NMT
            elif vars.minutos>= (params.min_desicion_cr1_c ):
                sell(
                app,
                vars,
                params,
                "C",
                "NMT",
                app.options[1]["contract"],
                app.options[1]["symbol"],
            )

                return


            # STOP LOSS
            elif vars.rentabilidad <= params.sl_cr1_c:
                sell(
                app,
                vars,
                params,
                "C",
                "SL",
                app.options[1]["contract"],
                app.options[1]["symbol"],
            )

            return

    #########################################################
    ####################      CALL F     ####################
    #########################################################
    elif vars.tipo == "F":
        # MANIFIESTA
        if vars.manifesto:

            # TARGET
            if vars.flag_target:
                if vars.rentabilidad < vars.pico:

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "TARGET",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return

            else:

                if vars.rentabilidad >= params.target_cf:
                    vars.flag_target = True
                # TIEMPO TERMINADO
                elif vars.minutos >= params.min_extras_cf:

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "NMT",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return
                # SL
                elif vars.rentabilidad <= params.sl_cf:

                    sell(
                        app,
                        vars,
                        params,
                        "C",
                        "SL",
                        app.options[1]["contract"],
                        app.options[1]["symbol"],
                    )

                    return
                else:
                    pass

        # AUN NO MANIFIESTA
        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umb_manifestacion_cf:
                vars.manifesto = True
                vars.minutos = 0
                if vars.rentabilidad >= params.target_cf:
                    vars.flag_target = True

            # FIN DE ESPERA
            elif vars.minutos >= params.min_desicion_cf:

                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "NMT",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return

            # SL
            elif vars.rentabilidad <= params.sl_cf:

                sell(
                    app,
                    vars,
                    params,
                    "C",
                    "SL",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

                return
            else:
                pass

    
    

    #########################################################
    ####################    CALL - U   ######################
    #########################################################
    elif vars.tipo == "U":

        if vars.rentabilidad <params.umbral_resta_cu and vars.rentabilidad <=(vars.pico-params.resta_cu[0])  :
            sell(
                    app,
                    vars,
                    params,
                    "C",
                    "NMR-U",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

            return
             
        elif   vars.rentabilidad >=params.umbral_resta_cu and vars.rentabilidad <=(vars.pico-params.resta_cu[1])  : 
            sell(
                    app,
                    vars,
                    params,
                    "C",
                    "NMR-U",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

            return
             
        elif vars.pico>=params.target_cu and vars.rentabilidad <=(vars.pico-params.retroceso_cu):
            sell(
                    app,
                    vars,
                    params,
                    "C",
                    "TARGET-U",
                    app.options[1]["contract"],
                    app.options[1]["symbol"],
                )

            return
            
        else:pass
    vars.regla_broadcasting=""

def sellPut(app, params, vars):

    timeNow = datetime.now(params.zone).time()

    # CALCULAR RENTABILIDAD
    if vars.askbid_put > params.max_askbid_venta:
        vars.rentabilidad = vars.pbid / vars.priceBuy - 1
        read_rentabilidad(vars)
        return
    if vars.pbid <= 0:
        return
    vars.rentabilidad = vars.pbid / vars.priceBuy - 1
    read_rentabilidad(vars)
    # CALCULAR RENTABILIDAD vars.pico
    if vars.pico < vars.rentabilidad:
        vars.pico = vars.rentabilidad

    vars.caida = vars.rentabilidad - vars.pico

    # # FIN DE DIA DE TRADE
 
    
    if timeNow >= params.fd:
        vars.venta_intentos=params.intentos
        sell(
            app,
            vars,
            params,
            "P",
            "FD",
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        return

    # REGLA PROTECCION
    if (
        vars.pico > params.umbral_no_perdida_p
        and vars.rentabilidad < (vars.pico - params.perdida_maxima_p)
        and vars.manifesto == False
    ):
        sell(
            app,
            vars,
            params,
            "P",
            "PROTECCION",
            app.options[2]["contract"],
            app.options[2]["symbol"],
        )

        return

    #########################################################
    ####################      PUT  R1     ###################
    #########################################################
    if vars.tipo == "R1":
        # UMBRAL
        if (
            (
                vars.dput > params.umbral_manifestacion_pu
                or vars.doput > params.umbral_manifestacion_pu
            )
            and vars.flag_umbral_pr1 == False
            and timeNow < params.timePut_umbral
        ):
            vars.flag_umbral_pr1 = True
            vars.ugs_n = 0

            vars.manifesto = True
            vars.tipo = "U"

        if vars.flag_umbral_pr1 == False:

            # MANIFIESTA
            if vars.manifesto:

                if vars.flag_target:
                    # TARGET AL PRIMER RETROCESO
                    if vars.rentabilidad < vars.pico:
                        sell(
                            app,
                            vars,
                            params,
                            "P",
                            "TARGET",
                            app.options[2]["contract"],
                            app.options[2]["symbol"],
                        )

                        return

                else:
                    # MANIFESTACION DEL TARGET
                    if vars.rentabilidad >= params.diamante_pr1[-1]:
                        vars.flag_target = True

                    else:
                        # DIAMANTE
                        for y in range(vars.ugs_n, len(params.diamante_pr1)):
                            if round(vars.pico, 3) > params.diamante_pr1[y]:
                                vars.ugs_n = y
                                if vars.ugs_n != vars.ugs_n_ant:
                                    vars.minutos = 0
                                    vars.ugs_n_ant = vars.ugs_n
                            else:
                                break

                        # RETROCEOS ABSOLUTO
                        if vars.ugs_n == 0:
                            if vars.rentabilidad <= params.retroceso_absoluto_pr1:
                                sell(
                                    app,
                                    vars,
                                    params,
                                    "P",
                                    "NMR",
                                    app.options[2]["contract"],
                                    app.options[2]["symbol"],
                                )

                                return

                        # RETROCESO
                        elif vars.rentabilidad <= (
                            vars.pico - params.resta_pr1[vars.ugs_n]
                        ):

                            name = f"T{vars.ugs_n}"
                            sell(
                                app,
                                vars,
                                params,
                                "P",
                                name,
                                app.options[2]["contract"],
                                app.options[2]["symbol"],
                            )

                            return

                        else:
                            pass

            # AUN NO MANIFIESTA
            else:

                # vars.manifesto
                if vars.rentabilidad >= params.umbral_manifestacion_pR1:
                    vars.manifesto = True
                    vars.minutos = 0

                # FIN DE ESPERA
                elif vars.minutos >= params.min_desicion_pr1:
                    sell(
                        app,
                        vars,
                        params,
                        "P",
                        "NMT",
                        app.options[2]["contract"],
                        app.options[2]["symbol"],
                    )

                    return

                # SL
                elif vars.rentabilidad <= params.sl_pr1:

                    sell(
                        app,
                        vars,
                        params,
                        "P",
                        "SL",
                        app.options[2]["contract"],
                        app.options[2]["symbol"],
                    )

                    return

                else:
                    pass

    #########################################################
    ####################      PUT  R1 -E  ###################
    #########################################################
    elif vars.tipo == "R1-E":

        if vars.manifesto:
            # # DIAMANTE
            # for y in range(vars.ugs_n, len(params.diamante_pr1e)):
            #     if round(vars.pico, 3) > params.diamante_pr1e[y]:
            #         vars.ugs_n = y
            #         if vars.ugs_n != vars.ugs_n_ant:
            #             vars.minutos = 0
            #             vars.ugs_n_ant = vars.ugs_n
            #     else:
            #         break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1e ):

                name = f"TARGET"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:
            # TOMA DE DESICION

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1e:
                vars.manifesto = True
                vars.minutos = 0

            # FIN DE ESPERA
            elif vars.minutos >= params.min_desicion_pr1e:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMT",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            # SL
            elif vars.rentabilidad <= params.sl_pr1e:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass


    #########################################################
    ####################      PUT  R1 - C  ###################
    #########################################################
    elif vars.tipo == "R1-C":

        if vars.manifesto:
 
            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr1c ):

                name = f"TARGET"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        # AUN NO MANIFIESTA
        else:
            # TOMA DE DESICION

            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR1c:
                vars.manifesto = True
                vars.minutos = 0

            # FIN DE ESPERA
            elif vars.minutos >= params.min_desicion_pr1c:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMT",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            # SL
            elif vars.rentabilidad <= params.sl_pr1c:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass
    #########################################################
    ####################      PUT  R2     ###################
    #########################################################
    elif vars.tipo == "R2":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pr2)):
                if round(vars.pico, 3) > params.diamante_pr2[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pr2[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pR2:
                vars.manifesto = True
                vars.minutos = 0

            # FIN DE ESPERA
            elif vars.minutos >= params.min_desicion_pr2:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMT",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            # SL
            elif vars.rentabilidad <= params.sl_pr2:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

    #########################################################
    ####################      PUT  M     ###################
    #########################################################
    elif vars.tipo == "M" or vars.tipo == "M2":
        # MANIFIESTA
        if vars.manifesto:

            # DIAMANTE
            for y in range(vars.ugs_n, len(params.diamante_pm)):
                if round(vars.pico, 3) > params.diamante_pm[y]:
                    vars.ugs_n = y
                    if vars.ugs_n != vars.ugs_n_ant:
                        vars.minutos = 0
                        vars.ugs_n_ant = vars.ugs_n
                else:
                    break

            # RETROCESO
            if vars.rentabilidad <= (vars.pico - params.resta_pm[vars.ugs_n]):

                name = f"T{vars.ugs_n}"
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    name,
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

        else:
            # vars.manifesto
            if vars.rentabilidad >= params.umbral_manifestacion_pm:
                vars.manifesto = True
                vars.minutos = 0

            
            # SL
            elif vars.rentabilidad <= params.sl_m:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return
    #########################################################
    ####################      PUT  F     ###################
    #########################################################
    elif vars.tipo == "F":
        # UMBRAL
        # if (
        #     (vars.doput > params.umbral_manifestacion_pu)
        #     and vars.flag_umbral_pf == False
        #     and timeNow < params.timePut_umbral
        # ):
        #     vars.flag_umbral_pf = True
        #     vars.ugs_n = 0

        #     vars.manifesto = True
        #     vars.tipo = "U"

        # if vars.flag_umbral_pf == False:
        # MANIFIESTA
        if vars.manifesto:

            if vars.flag_target:
                # TARGET AL PRIMER RETROCESO
                if vars.rentabilidad < vars.pico - params.resta_pf:
                    sell(
                        app,
                        vars,
                        params,
                        "P",
                        "TARGET",
                        app.options[2]["contract"],
                        app.options[2]["symbol"],
                    )

                    return

            else:
                # MANIFESTACION DEL TARGET
                if vars.rentabilidad >= params.target_pf:
                    vars.flag_target = True

            if vars.rentabilidad <= params.proteccion_pf:
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMR",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )
                return

        # AUN NO MANIFIESTA
        else:

            # vars.manifesto
            if vars.rentabilidad >= params.umb_manifestacion_pf:
                vars.manifesto = True
                vars.minutos = 0
                if vars.rentabilidad >= params.target_pf:
                    vars.flag_target = True

            # FIN DE ESPERA
            elif vars.minutos >= params.min_desicion_pf:
                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMT",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            # SL
            elif vars.rentabilidad <= params.sl_pf:

                sell(
                    app,
                    vars,
                    params,
                    "P",
                    "SL",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

                return

            else:
                pass

   

    #########################################################
    ####################       PUT - U   ####################
    #########################################################
    elif vars.tipo == "U":

        if vars.rentabilidad <params.umbral_resta_pu and vars.rentabilidad <=(vars.pico-params.resta_pu[0])  :
            sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMR-U",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

            return
        elif   vars.rentabilidad >=params.umbral_resta_pu and vars.rentabilidad <=(vars.pico-params.resta_pu[1])  : 
            sell(
                    app,
                    vars,
                    params,
                    "P",
                    "NMR-U",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

            return
        elif vars.pico>=params.target_pu and vars.rentabilidad <=(vars.pico-params.retroceso_pu):
            sell(
                    app,
                    vars,
                    params,
                    "P",
                    "TARGET-U",
                    app.options[2]["contract"],
                    app.options[2]["symbol"],
                )

            return
        else:pass
 
    vars.regla_broadcasting=""
     
def sell(app, vars, params, tipo, regla, contract, symbol):
    from rules.routine import calculations
    if vars.rentabilidad<0:
        vars.regla_broadcasting = regla
        respuesta=verificar_regla(params)
        if respuesta==False: return


    if vars.sell_broadcasting ==False:
        asyncio.run(send_sell(app, vars, params, tipo,regla))
 
 

    # LECTURA PREVIA
    readIBData_action(app, vars, tipo, regla)

    # ENVIO DE ORDEN DE VENTA
    flag = sellOptionContract(params, app, vars, tipo, contract, symbol)
    if flag == False:
        printStamp("-NO SE PUDO CONCRETAR LA VENTA-")
        return False

    # ESPERA DE LA ORDEN DE VENTA
    app.statusIB = False
    app.Error = False

    printStamp("-wait Status-")

    while app.statusIB == False:

        timeNow = datetime.now(params.zone).time()

        if int(timeNow.second) in params.frecuencia_muestra:
            calculations(app, vars, params)
            # ESPERANDO Y REGISTRANDO
            vars.status = "SELLING"
            saveJson(vars, app, params, False)
            writeDayTrade(app, vars, params)

        if app.Error:
            break
        time.sleep(1)
    if app.Error:
        printStamp(f"-VENTA NO PROCESADA-")
        sendError(params, "VENTA NO PROCESADA")
        return False

    # SET DE VARIABLES
    vars.regla = regla
    vars.regla_ant = vars.regla
    if tipo == "C":
        vars.call = False
    elif tipo == "P":
        vars.put = False

    vars.status = "SLEEP"
    read_sell(vars, tipo)
    return True