# ====================
#  - Librerias -
# ====================
import json
import os
from functions.logs import printStamp


###############################################
#                  VARIABLES
###############################################
class variables:
    def __init__(self):
        ###############################################
        # LECTURA DEL ARCHIVO DE VARIABLES
        ###############################################

        file_name = "/usr/src/app/data/vars.json"

        if os.path.exists(file_name):
            # Leer el archivo JSON
            with open(file_name, "r") as json_file:
                self.data = json.load(json_file)
                printStamp(" - Lectura de archivo de variables - ")
        else:
            printStamp(" - No se encuentra archivo de variables - ")
            exit()

        ###############################################
        # VARIABLES DE APP
        ###############################################

        self.cash = self.data.get("cash", 0)
        self.statusIB = self.data.get("statusIB", False)
        self.execution_details = self.data.get("execution_details", {})
        self.commissions = self.data.get("commissions", {})
        self.sendError = self.data.get("sendError", False)
        self.Error = self.data.get("Error", False)
        self.Error_buy = self.data.get("Error_buy", False)

        ###############################################
        # VARIABLES DE TIEMPO
        ###############################################
        self.minutos = self.data.get("minutos", 0)
        self.n_minutos = self.data.get("n_minutos", 0)
        self.minutos_trade = self.data.get("minutos_trade", 0)

        ###############################################
        # VARIABLES DE PRECIO
        ###############################################
        self.call_close = self.data.get("call_close", 0)
        self.put_close = self.data.get("put_close", 0)
        self.call_open = self.data.get("call_open", 0)
        self.put_open = self.data.get("put_open", 0)

        ###############################################
        # VARIABLES DE FLAGS
        ###############################################
        self.call = self.data.get("call", False)
        self.put = self.data.get("put", False)
        self.compra = self.data.get("compra", True)
        self.manifesto = self.data.get("manifesto", False)

        self.flag_Call_R2 = self.data.get("flag_Call_R2", False)
        self.flag_Put_R2 = self.data.get("flag_Put_R2", False)
        self.flag_Call_reset_r1 = self.data.get("flag_Call_reset_r1", False)
        self.flag_Put_reset_r1_i = self.data.get("flag_Put_reset_r1_i", False)
        self.flag_Put_reset_r1 = self.data.get("flag_Put_reset_r1", False)

 
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
        self.min_extras = self.data.get("min_extras", 0)
        self.min_desicion = self.data.get("min_desicion", 0)
        self.ugs_n = self.data.get("ugs_n", 0)
        self.ugs_n_ant = self.data.get("ugs_n_ant", 0)
        self.pico = self.data.get("pico", 0)
        self.tipo = self.data.get("tipo", "")

        ###############################################
        # VARIABLES DE TRADING
        ###############################################
        self.vix= self.data.get("vix", 0)
        self.dcall = self.data.get("dcall", 0)
        self.dput = self.data.get("dput", 0)
        self.docall = self.data.get("docall", 0)
        self.doput = self.data.get("doput", 0)
        self.askbid_call = self.data.get("askbid_call", 0)
        self.askbid_put = self.data.get("askbid_put", 0)
        self.quantity = self.data.get("quantity", 0)
        self.rentabilidad = self.data.get("rentabilidad", 0)
        self.rentabilidad_ant = self.data.get("rentabilidad_ant", 0)
        self.priceBuy = self.data.get("priceBuy", 0)
        self.real_priceBuy = self.data.get("real_priceBuy", 0)
        self.caida = self.data.get("caida", 0)
        self.regla = self.data.get("regla", "")
        self.trades = self.data.get("trades", [])
        self.fecha = self.data.get("fecha", "")
        self.strikes = self.data.get("strikes", {})
        self.strike_c = self.data.get("strike_c", 0)
        self.strike_p = self.data.get("strike_p", 0)
        self.dif_exp = self.data.get("dif_exp", 0)
        self.dic_strike = self.data.get("dic_strike", 0)
        self.exp = self.data.get("exp", "")
        self.rentabilidad_final = 0
        self.dic_exp_strike = self.data.get("dic_exp_strike", {})
        self.rule = self.data.get("rule", True)
        self.cask = 0
        self.cbid = 0
        self.pask = 0
        self.pbid = 0
        self.regla_ant = ""
        self.trade_hour = ""
        self.accion_mensaje = self.data.get("accion_mensaje", 0)
        self.bloqueo = self.data.get("bloqueo", True)
        self.exchange = self.data.get("exchange", "CBOE")
        self.status = self.data.get("status", "ON")

        ###############################################
        # BROADCASTING
        ###############################################
        self.hora_inicio = self.data.get("hora_inicio", "")
        self.aliniar = self.data.get("aliniar", False)
        self.sell_broadcasting = self.data.get("sell_broadcasting", False)
        self.sell_tipo_broadcasting = self.data.get("sell_tipo_broadcasting", "")
        self.sell_regla_broadcasting = self.data.get("sell_regla_broadcasting", "")
        self.buy_broadcasting = self.data.get("buy_broadcasting", False)
        self.buy_tipo_broadcasting = self.data.get("buy_tipo_broadcasting", "")
        self.buy_regla_broadcasting = self.data.get("buy_regla_broadcasting", "")
        self.user_broadcasting = self.data.get("user_broadcasting", "")
        self.conexion = self.data.get("conexion", True)
        self.venta_intentos= self.data.get("venta_intentos", 0)
        self.regla_broadcasting = self.data.get("regla_broadcasting", "")


        ###############################################
        # LABEL
        ###############################################

        self.label = self.data.get("label", True)
        self.retorno = self.data.get("retorno", 0)
        self.signo  = self.data.get("signo", "")
        self.varianza  = self.data.get("varianza", "")

 