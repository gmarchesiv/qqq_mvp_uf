# ====================
#  - Librerias -
# ====================
import json
import os
from functions.logs import printStamp
from collections import deque

###############################################
#                  VARIABLES
###############################################
class varsRutina:
    def __init__(self,debug_mode ):

        #---------------------------------------------------
        '''
        Abriremos el archivo json Correspondientes 
        (vars.json) y en caso no exista la variable la genera,
        finalmente la carga en memoria.
        '''
        #---------------------------------------------------
        if debug_mode ==False:
            file_name = "/usr/src/app/data/vars.json"

            if os.path.exists(file_name):
                # Leer el archivo JSON
                with open(file_name, "r") as json_file:
                    self.data = json.load(json_file)
                    printStamp(" - Lectura de archivo de variables - ")
            else:
                printStamp(" - No se encuentra archivo de variables - ")
                exit()
        else:
            self.data={}

            
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
        self.name =self.data.get("name", "") 
        self.wallet =self.data.get("wallet", {}) 
        self.conexion = False # indica conexcion al sistema 
        self.ready = False  # Indica que se encuentra en Rutina
        self.flag_alerta=False # envia alerta de desconexcion
        self.fecha = self.data.get("fecha", "") # Fecha 
        self.date= self.data.get("fecha", "")
        self.time= self.data.get("time", "")
        self.trades = self.data.get("trades", []) # Trades Hechos
        self.flag_bloqueo_tiempo= self.data.get("flag_bloqueo_tiempo", False) # Bloqueo Por Tiempo
        self.bloqueo = True # Bloqueo Por Trades
        self.accion_mensaje = self.data.get("accion_mensaje", 0) # cambios de mensaje compra y venta
        self.exchange = self.data.get("exchange", "CBOE")
        self.hora_inicio = self.data.get("hora_inicio", "") # Hora de inicio
        self.status = self.data.get("status", "ON") # Status
        self.df=None # Data Frame Debug
        self.i=0 # posicion debug
        ###############################################
        # VARIABLES DE TIEMPO
        ###############################################
        self.minutos = self.data.get("minutos", 0)
        self.n_minutos = self.data.get("n_minutos", 0)
        self.minutos_trade = self.data.get("minutos_trade", 0)

        ###############################################
        # VARIABLES DE TRADING
        ###############################################

         # ETF 

        self.vix= self.data.get("vix", 0)
        self.price= self.data.get("price", 0)


        # OPTION

        self.exp = self.data.get("exp", "")
        self.quantity = self.data.get("quantity", 0)
        self.priceBuy = self.data.get("priceBuy", 0)
        self.real_priceBuy = self.data.get("real_priceBuy", 0)
        self.params_regla=self.data.get("params_regla", "")
        self.rentabilidad = self.data.get("rentabilidad", 0)
        self.rentabilidad_ant = self.data.get("rentabilidad_ant", 0)
        self.regla = self.data.get("regla", "")
        self.ugs_n = self.data.get("ugs_n", 0)
        self.ugs_n_ant = self.data.get("ugs_n_ant", 0)
        self.pico = self.data.get("pico", 0)
        self.tipo = self.data.get("tipo", "")
        self.call_dic= self.data.get("call_dic",{})
        self.put_dic= self.data.get("put_dic", {})
        self.caida = self.data.get("caida", 0)
        self.trade_hour = ""
        self.regla_ant = ""
            # CALL
        self.strike_c = self.data.get("strike_c", 0)
        self.dcall = self.data.get("dcall", 0)
        self.docall = self.data.get("docall", 0)
        self.askbid_call = self.data.get("askbid_call", 0)
        self.askbid_call_prom = self.data.get("askbid_call_prom ", [])
        self.askbid_call_prom=deque(self.askbid_call_prom, maxlen=89)
        self.call_close = self.data.get("call_close", 0)
        self.call_open = self.data.get("call_open", 0)
        self.cask = 0
        self.cbid = 0
        self.price_Call_label=self.data.get("price_Call_label", 0)
        self.d_Call_label=self.data.get("d_Call_label", 0)
        self.promedio_call=self.data.get("promedio_call",0)
        
            # PUT
        self.strike_p = self.data.get("strike_p", 0)
        self.dput = self.data.get("dput", 0)  
        self.doput = self.data.get("doput", 0)
        self.doput_ant = self.data.get("doput_ant", 0)    
        self.askbid_put = self.data.get("askbid_put", 0)
        self.askbid_put_prom  = self.data.get("askbid_put_prom ",[]) 
        self.askbid_put_prom=deque(self.askbid_put_prom, maxlen=89)
        self.put_close = self.data.get("put_close", 0)
        self.put_open = self.data.get("put_open", 0)
        self.pask = 0
        self.pbid = 0
        self.price_Put_label=self.data.get("price_Put_label", 0)
        self.d_Put_label=self.data.get("d_Put_label", 0)
        self.promedio_put=self.data.get("promedio_put",0)


        ###############################################
        # VARIABLES DE FLAGS
        ###############################################
        self.call = self.data.get("call", False)
        self.put = self.data.get("put", False)
        self.compra = self.data.get("compra", True)

        self.flag_real_priceBuy = self.data.get("flag_real_priceBuy", False)


        self.rule = self.data.get("rule", True) # para muestra de R2
        self.flag_Call_R2 = self.data.get("flag_Call_R2", False)
        self.flag_Put_R2 = self.data.get("flag_Put_R2", False)
        self.flag_cambio_R1_label= self.data.get("flag_Put_R2", False)
        self.flag_Call_label_cambio= self.data.get("flag_Call_label_cambio", False)
        self.flag_Call_label_1_compra= self.data.get("flag_Call_label_1_compra", False) 
        self.flag_Call_label_2_compra= self.data.get("flag_Call_label_2_compra", False) 

        self.flag_Call_reset= self.data.get("flag_Call_reset",   {
                "R1":False,
                "R1-3":False,
                "R1-E":False,
                "R1-E2":False,
                "INV":False,
                "R1-C":False,
                "F1":False,
                "FAST_2":False
            })
        self.flag_Put_reset=self.data.get("flag_Put_reset", {
                "FAST":False,
                "R2-FAST":False,
                "R2":False,
                "R2-E":False,
                "R3":False
            })
        
        self.flag_Put_reset_esc=self.data.get("flag_Put_reset_esc", {
                "LABEL-1":False,
                "LABEL-2":False
            })
        self.flag_cambio_fast= self.data.get("flag_Put_R2", False)
        self.flag_Put_label_cambio= self.data.get("flag_Put_label_cambio", False)
        self.flag_bloqueo_put=self.data.get("flag_bloqueo_put", False)
        self.flag_bloqueo_r1_e= self.data.get("flag_bloqueo_r1_e", False)
        
       
        
        ###############################################
        # VARIABLES DE RUTINA
        ###############################################
    
        
        
        
        
        
        
        
        

 
 
        


        

 

        if debug_mode ==False:
            file_name = "/usr/src/app/data/vars.json"
            with open(file_name, "r") as file:
                datos = json.load(file)
    
                datos["bloqueo"] = True
        
            with open(file_name, "w") as file:
                json.dump(datos, file, indent=4)