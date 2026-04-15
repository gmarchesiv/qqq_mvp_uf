# ====================
#  - Librerias -
# ====================
import json
import os
import pytz
from dotenv import load_dotenv
from datetime import time as dt_time
from functions.logs import printStamp


###############################################
#                  PARAMETROS
###############################################
class parameters:
    def __init__(self,debug_mode):

        #---------------------------------------------------
        '''
        Cargamos los parametros del modelo a memoria.
        '''
        #---------------------------------------------------

        ###############################################
        #               PARAMETROS -  GENERALES
        ###############################################

        self.etf = "QQQ"
        self.exchange = ["SMART"]
        self.zone = pytz.timezone("America/New_York")

        ###############################################
        #               PARAMETROS -  DEL ENV
        ###############################################

        load_dotenv()
        self.name = os.getenv("NAMEIB")
        self.tele = os.getenv("TELEID")
        self.token = os.getenv("TOKENBOT")
        self.typeIB = os.getenv("TYPEIB")
        self.cuenta = os.getenv("CUENTA")
 
        ###############################################
        #               PARAMETROS -  conexión IBKR
        ###############################################

        self.ip = "ibkr"  # IP de conexion de contenedores
        self.port = 8888  #  Puerto de conexion con datos IBKR
        self.time_connection = 180  # Tiempo para probar la conexion (Segundos)
        self.client = 123  # Numero de Cliente del modelo

        ###############################################
        #               PARAMETROS -  BoradCasting
        ###############################################

        if debug_mode == False :
            file_name = "/usr/src/app/data/grupo.json"

            if os.path.exists(file_name):
                # Leer el archivo JSON
                with open(file_name, "r") as json_file:
                    self.data = json.load(json_file)
                    printStamp(" - Lectura de archivo de Grupos - ")
            else:
                printStamp(" - No se encuentra archivo de Grupos - ")
                exit()
            self.users = self.data["red"]

        ###############################################
        #               PARAMETROS -  RUTINA
        ###############################################

        # PARAMETROS NO DEFINIDOS
        self.inf = 999
        self.inf_n = -9
 
        # SELECCION DE STRIKES 
        self.rangos_strikes = [[2, 2.6] ]
        self.days_min_exp = 31  # DIAS para el exp minimo de busqueda
        self.days_max_exp = 39 
        self.except_days_min_exp = 26

        # PARAMETROS DE ASKBID DE ACCIONES
        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028
        self.max_askbid_venta_abs = 0.0255
        self.max_askbid_compra_abs = 0.0185
        self.max_askbid_compra_alt = 0.02
        self.max_askbid_venta_forzada = 0.04

        # PARAMETROS LIMITES DE OPEN ASKBID
        self.max_askbid_open = 0.03
        self.max_askbid_hora_open =  dt_time(9, 33)
        self.umbral_askbid=0.08
        self.limite_Put_bloqueo=[-0.1,0.2]
        # PARAMETROS DE COMPRA VENTA SLIPPAGE
        self.slippage=1.04

        #PARAMETROS DE TIEMPO DE RUTINA Y MUESTRAS
        self.fin_rutina = dt_time(15, 55)
        self.fd =  dt_time(15, 45)
        self.rutina = [dt_time(6, 50), dt_time(16, 0)]
        self.frecuencia_accion =[i for i in range(0, 60, 2)]
        
        #PARAMETROS DE VENTA 
        self.intentos=1
        self.tiempo_contulta=5

        #PARAMETROS DE PROTECCION
        self.proteccion_ask_bid=[[dt_time(9, 45,0), dt_time(9, 45,18)],[dt_time(10, 0,0), dt_time(10,0,30 )]]
        self.proteccion_compra=[ dt_time(9, 44,20), dt_time(9, 46,0) ]
        self.proteccion_compra_2=[ dt_time(9, 59,30), dt_time(10, 0,15) ]
        self.proteccion_compra_call_r1=[ dt_time(9, 44,0), dt_time(9, 45,40)  ]
        self.proteccion_compra_r2=[ dt_time(9, 44,20), dt_time(9, 45,15) ]
        
        #########################################################
        ####################      CALL        ###################
        #########################################################
        # ==================================
        # =========== CALL PROTECCION ======  
        # ==================================
        self.umbral_no_perdida_c = 0.016
        
        self.perdida_maxima_c = 0.045
    
        self.perdida_maxima_c_abs = -0.017

        self.umbral_no_perdida_c_r2 = 0.016
        self.perdida_maxima_c_r2 = 0.05
       

        #########################################################
        ####################      PUT         ###################
        #########################################################

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.015
        
        self.perdida_maxima_p = 0.05
    
        self.perdida_maxima_p_abs = -0.017

        self.umbral_no_perdida_p_r2 = 0.016
        self.perdida_maxima_p_r2 = 0.04
   
       
        #########################################################
        ####################      LABELS      ###################
        #########################################################
        
        self.omega=0.00000297000000
        self.alpha=0.027400000
        self.beta=0.90520000
        self.gamma=0.11470000
        self.days_year=252




#################################################################
# ▒█▀▀█ ░█▀▀█ ▒█░░░ ▒█░░░ ░░ ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█ ▒█░░░ ░█▀▀█ ▒█▀▀▀█ 
# ▒█░░░ ▒█▄▄█ ▒█░░░ ▒█░░░ ▀▀ ▒█▄▄▀ ▒█▀▀▀ ▒█░▄▄ ▒█░░░ ▒█▄▄█ ░▀▀▀▄▄ 
# ▒█▄▄█ ▒█░▒█ ▒█▄▄█ ▒█▄▄█ ░░ ▒█░▒█ ▒█▄▄▄ ▒█▄▄█ ▒█▄▄█ ▒█░▒█ ▒█▄▄▄█
#################################################################
class call_params:
    def __init__(self):
        inf = 999
        inf_n = -9
        ######################################################### COMENTAR EN LIVE
        self.r1={
            "REGLA":"R1",
            "D":[0.11, 0.1265],
            "DO":[0.028, 0.035],
            "DPUT":[-0.21, -0.092],
            "TIME":[dt_time(9, 37), dt_time(9,48)],
            "LABEL":0,

            "SL":-0.035 ,
            "DIAMANTE":[0.0165 ,0.0275 ,0.04  ],
            "RESTA":[ 0.01 ,0.005, 0.001],
            
            "NMT":inf,
            "TARGET_NMT":inf
            } 

        #########################################################
        self.r1_2={
            "REGLA":"R1-2",
            "D":[0 , 0.08],
            "DO":[0.03, 0.034],
            "DPUT":[ -0.17 ,-0.06 ], 
            "TIME":[dt_time(9, 34), dt_time(9, 38,15)],
            "LABEL":0,

            "SL":-0.036 ,
            "DIAMANTE":[0.0165,0.028 ,0.0379 ,0.07,0.1 ],
            "RESTA":[ 0.012,0.01,0.005,0.02 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            } 
        
    
        #########################################################
        self.r1_3={
            "REGLA":"R1-3",
            "D":[0.06, 0.09],
            "DO":[-0.014, 0.025 ],
            "DPUT":[ -0.145 ,-0.05 ], 
            "TIME":[dt_time(9, 40), dt_time(9, 43)],
            "LABEL":0,

            "SL":-0.05 ,
            "DIAMANTE":[0.0165,0.028 ,0.0379 ,0.07,0.1 ],
            "RESTA":[ 0.012,0.01,0.005,0.02 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            } 
        #########################################################
        self.r1_e={
            "REGLA":"R1-E",
            "D":[-0.155,0.1 ],
            "DO": [0.057, 0.06],
            "DPUT":[ -0.175 ,0.035 ],
            "TIME":[dt_time(10,14), dt_time(10, 35)],
            "LABEL":0,
            "BLOQUEO_TIME":dt_time(10,0),
            "BLOQUEO_DOCALL":0.15,
            "BLOQUEO_DOPUT":0.062,

            "SL":-0.046,
            "DIAMANTE":[0.0165,0.027,0.0379, 0.07 ],
            "RESTA":[0.015,0.01,0.005, 0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
    
        #########################################################
        self.inv={
            "REGLA":"INV",
            "D":[-0.245, 0.03],
            "DO":[0.07, 0.078 ],
            "DPUT":[ -0.055 ,0.28 ],
    
            "TIME":[dt_time(9, 34), dt_time(9,39)],
            "LABEL":1,
            

            "SL":-0.045,
            "DIAMANTE":[0.018,0.0245,0.03],
            "RESTA": [0.015,0.01 ,0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        
        
        #########################################################
        self.r2={
            "REGLA":"R2",
            "D":[0.24, 0.445],
            "DO":[0.028, 0.0335],
            "DPUT":[ -0.41 ,-0.19 ],
            "TIME":[dt_time(9, 36,30), dt_time(9, 50)],
            "LABEL":0,
            "UMBRAL_R2":0.225,      
    
            "SL":-0.05 ,
            "DIAMANTE":[0.023,0.025  ],
            "RESTA":[0.015 ,0.001],
            "NMT":60,
            "TARGET_NMT":0.01
            }
        #########################################################  COMENTAR EN LIVE
        self.r2_2={
            "REGLA":"R2-2",
            "D":[0.25, 0.40],
            "DO":[0.03, 0.0335] ,
            "DPUT":[ -0.4 ,-0.17 ],
            "TIME":[dt_time(10, 0), dt_time(10, 30)],
            "LABEL":0,

            "SL":-0.05 ,
    
            "DIAMANTE":[0.02,0.03,0.05  ],
            "RESTA":[0.01, 0.005  ,0.001],
            "NMT":60,
            "TARGET_NMT":0.01
            }
        #########################################################
        self.fast={
            "REGLA":"FAST",
            "D":[-0.02 ,0.08],
            "DO": [0.04, 0.057] ,
            "DPUT":[ -0.15 ,0.03],
            "TIME":[dt_time(9, 42), dt_time(9, 52)],
            "LABEL":0,

            "SL":-0.045,
            "DIAMANTE":[0.02,0.025,0.04 ] ,
            "RESTA":[0.01,0.005 ,0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.r3={
            "REGLA":"R3",
            "D":[ 0.19, 0.225],
            "DO": [0.03, 0.04],
            "DPUT":[ -0.21 ,-0.135 ],
            "TIME": [dt_time(9, 38), dt_time(9, 52)],
            "LABEL":0,

            "SL":-0.046,
            "DIAMANTE":[0.0165,0.02 , 0.025] ,
            "RESTA":[0.015,0.003,0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################  COMENTAR EN LIVE
        self.f1={
            "REGLA":"F1",
            "D":[-0.05,0.06],
            "DO":[0.0315, 0.04],
            "DPUT":[ -0.105 ,0.02 ],
            "TIME":[dt_time(14, 30), dt_time(14, 45)],
            "LABEL":0,


            "SL":-0.035,
            "DIAMANTE":[0.015, 0.02,0.025],
            "RESTA":   [0.01 ,0.003,0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################  
        self.fast_2={
            "REGLA":"FAST_2",
            "D":[-0.19, 0.15],
            "DO":[0.048, 0.056],
            "DPUT":[ -0.23,0.135 ],  
            "TIME":[dt_time(9, 35), dt_time(9, 37)],
            "LABEL":0,


            "SL":-0.045,
            "DIAMANTE":[0.02,0.03,0.04,0.06] ,
            "RESTA":[0.015,0.01,0.005,0.001] ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        
        #########################################################
        self.label_1={
            "REGLA":"LABEL-1",
            "D":[ -0.21, -0.1],
            "DO":[-0.17, 0.045],
            "DPUT":[0.05, 0.265],
        
            "TIME":[dt_time(10, 20), dt_time(10, 40,5)],
            "TIME-FIN":dt_time(10, 45),
            "LABEL":0,

            "UMBRAL_COMPRA":[0.002,0.005],

            "SL":-0.035,
            "DIAMANTE":[0.014,0.025 ,0.03,0.04],
            "RESTA":[0.014,0.005  , 0.003  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.label_2={
            "REGLA":"LABEL-2",
            "D":[ -0.085, 0.175],
            "DO":[-0.05, 0.05],
            "DPUT":[-0.135, 0.07],
        
            "TIME":[dt_time(9, 45), dt_time(9, 55,5)],
            "TIME-FIN":dt_time(10, 0),
            "LABEL":0,

            "UMBRAL_COMPRA":[0.002,0.005],

            "SL":-0.035,
            "DIAMANTE":[0.013,0.025 ,0.03,0.04],
            "RESTA":[0.01 ,0.005  , 0.003  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }


###########################################################
# ▒█▀▀█ ▒█░▒█ ▀▀█▀▀ ░░ ▒█▀▀█ ▒█▀▀▀ ▒█▀▀█ ▒█░░░ ░█▀▀█ ▒█▀▀▀█ 
# ▒█▄▄█ ▒█░▒█ ░▒█░░ ▀▀ ▒█▄▄▀ ▒█▀▀▀ ▒█░▄▄ ▒█░░░ ▒█▄▄█ ░▀▀▀▄▄ 
# ▒█░░░ ░▀▄▄▀ ░▒█░░ ░░ ▒█░▒█ ▒█▄▄▄ ▒█▄▄█ ▒█▄▄█ ▒█░▒█ ▒█▄▄▄█
###########################################################
class put_params:
    def __init__(self):
        inf = 999
        inf_n = -9


        ######################################################### COMENTAR EN LIVE
        self.inv_2={
            "REGLA":"INV-2",
            "D":[-0.28, -0.21],
            "DO":[0.025, 0.046],
            "DCALL":[0.2,0.385],
            "TIME":[dt_time(9,33,30), dt_time(9,36)],
            "LABEL":0,

            "SL":-0.05,
            "DIAMANTE":[0.018, 0.025 ,0.0295],
            "RESTA":[0.015 , 0.01,0.001 ],

            
            "NMT":inf,
            "TARGET_NMT":inf
            }
        

        #########################################################
        self.inv_3={
            "REGLA":"INV-3",
            "D":[-0.03, 0.075],
            "DO":[0.0645, 0.074],
            "DCALL":[-0.14,0.023],
            "TIME":[dt_time(9,35), dt_time(9,59)],
            "LABEL":0,

            "SL":-0.04,
            "DIAMANTE":[0.018, 0.025 ,0.0295],
            "RESTA":[0.017 , 0.01,0.001 ],

            
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.inv_4={
            "REGLA":"INV-4",
            "D":[-0.035, -0.01],
            "DO":[0.03, 0.0335],
            "DCALL":[-0.03 , 0.075],
            "TIME":[dt_time(9,35), dt_time(9,58)],
            "LABEL":0,

            "SL":-0.045,
            "DIAMANTE":[0.018,0.023,0.04 ],
            "RESTA":[0.012 ,0.0045 ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.inv_5={
            "REGLA":"INV-5",
            "D":[-0.19, -0.129],
            "DO":[0.03, 0.0375],
            "DCALL":[-0.005,0.24],
            "TIME":[dt_time(9,35,20), dt_time(9,50,20)],
            "LABEL":0,

            "SL":-0.045,
            "DIAMANTE":[0.0165,0.025,0.03,0.04],
            "RESTA":[0.012,0.01 , 0.005,0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.inv_6={
            "REGLA":"INV-6",
            "D":[-0.6, -0.35],
            "DO":[0.02, 0.03 ],
            # "DCALL":[-0.005,0.24],
            "TIME":[dt_time(9,35), dt_time(9,45)],
            "LABEL":0,

            "SL":-0.05,
            "DIAMANTE":[0.0165,0.025,0.03,0.04],
            "RESTA":[0.012,0.01 , 0.005,0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.fast={
            "REGLA":"FAST",
            "D":[ 0.08, 0.158],
            "DO":[0.081, 0.087],
            "DCALL":[ -0.21,-0.08],
            "TIME":[dt_time(9, 40), dt_time(9, 50)],
    
            "LABEL":1,

            "SL":-0.035,
            "DIAMANTE":[0.02,  0.03 ,0.065,0.075  ],
            "RESTA":[0.005, 0.011 ,0.02 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.label_1={
            "REGLA":"LABEL-1",
            "D":[ 0.024, 0.10],
            "DO":[0.03, 0.04],
            "DCALL":[-0.195 , -0.04],
            "TIME":[dt_time(9, 40), dt_time(9, 45)],
            "LABEL":1,

            "SL":-0.04,
            "DIAMANTE":[0.0165,0.025 ,0.04,0.07,0.08],
            "RESTA":[0.015,0.01  ,0.008  ,0.005  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################  
        self.label_2={
            "REGLA":"LABEL-2",
            "D":[ 0.024, 0.105],
            "DO":[0.03, 0.04],
            "DCALL":[-0.195 , -0.03], 
            
            "TIME":[dt_time(9, 50), dt_time(10, 32)],
            "LABEL":1,

            "SL":-0.046,
            "DIAMANTE":[0.0165,0.025 ,0.04,0.07,0.08],
            "RESTA":[0.015,0.01  ,0.008  ,0.005  ,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        

        #########################################################  
        self.label_4={
            "REGLA":"LABEL-4",
            "D":[ -0.335, 0.08],
            "DO":[-0.14, 0.265],
            "DCALL":[-0.06 , 0.335], 
            "UMBRAL_COMPRA":[0.002,0.005],
            "TIME":[dt_time(10, 40), dt_time(11, 15,5)],
            "TIME-FIN":dt_time(11, 20),
            "LABEL":1,

            "SL":-0.05,
            "DIAMANTE":[ 0.02 ,0.024 ,0.03 ,0.04 ],
            "RESTA":[ 0.01 , 0.005 , 0.003 , 0.001],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.r2={
            "REGLA":"R2",
            "D":[0.168,0.32] ,
            "DO": [0.0545, 0.063 ] ,
            "DCALL":[-0.335 , -0.1],
            "TIME":[dt_time(9, 45),dt_time(10, 27)],
            "LABEL":1,
            "UMBRAL_R2":0.15,  


            "SL":-0.05,
            "DIAMANTE":[0.02,  0.03 ,0.065,0.08,0.098 ],
            "RESTA":[0.015, 0.012 ,0.02 ,0.005,0.001],


            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTAR EN LIVE
        self.r2_e={
            "REGLA":"R2-E",
            "D":[0.385, 0.57] ,
            "DO": [0.0355, 0.055]  ,
            "DCALL":[0. , 0.], # NO DEFINIDO
            "TIME":[dt_time(9, 50), dt_time(9, 55)],
            "LABEL":1,
        

            "SL":-0.045,
            "DIAMANTE":[0.0165,0.025 ] ,
            "RESTA":[0.012 ,0.001] ,
            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTAR EN LIVE
        self.r2_fast={
            "REGLA":"R2-FAST",
            "D":[ 0.295, 0.42],
            "DO":[0.0545, 0.06 ],
            "DCALL":[-0.395 , -0.23],
            "TIME": [dt_time(9, 34), dt_time(9, 35,30)],
            "LABEL":1,
        

            "SL":-0.045,
            "DIAMANTE":[0.0165,0.025,0.04] ,
            "RESTA":[0.01,0.005,0.001 ],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTAR EN LIVE
        self.f1={
            "REGLA":"F1",
            "D":[0,0.52],
            "DO":[0.05, 0.059],
            "DCALL":[-0.38 , -0.06],
            "TIME":[dt_time(12, 30), dt_time(12, 46)],
            "LABEL":1,


            "SL":-0.04,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        

        #########################################################
        self.r3={
            "REGLA":"R3",
            "D":[ 0.06, 0.138],
            "DO": [0.0191, 0.023],
            "DCALL":[ -0.23 ,-0.09 ],
            "TIME": [dt_time(9, 40), dt_time(9, 45)],
            "LABEL":1,

            "SL":-0.052,
            "DIAMANTE":[0.0165,0.027 , 0.04,0.06,0.09] ,
            "RESTA":[0.014,0.005,0.003,0.001,inf_n],
            "NMT":inf,
            "TARGET_NMT":inf
            }
        #########################################################
        self.f_inv_1={
            "REGLA":"F-INV-1",
            "D":[0.144,0.233],
            "DO":[-0.186, 0.062],
            "DCALL":[-0.278 , -0.143],
            "TIME":[dt_time(14, 30), dt_time(14, 32)],
            "LABEL":0,


            "SL":-0.05,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        
        #########################################################
        self.f_inv_2={
            "REGLA":"F-INV-2",
            "D":[-0.62,-0.3],
            "DO":[-0.38, 0],
            "DCALL":[0.1, inf],
            "TIME":[dt_time(14, 30), dt_time(14, 35)],
            "LABEL":0,


            "SL":-0.05,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":15,
            "TARGET_NMT":0
            }
        
        #########################################################
        self.f_inv_3={
            "REGLA":"F-INV-3",
            "D":[-0.147,-0.037],
            "DO":[-0.116, -0.05],
            "DCALL":[0.04 , 0.143],
            "TIME":[dt_time(14, 30), dt_time(14, 35)],
            "LABEL":0,


            "SL":-0.05,
            "DIAMANTE":[0.0165, 0.02 ,0.025 ],
            "RESTA":   [0.005 , 0.003,0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }


        ######################################################### COMENTAR EN LIVE
        self.f2={
            "REGLA":"F2",
            "D":[-0.015,0.21],
            "DO":[-0.155, 0.1],
            "DCALL":[-0.21 , 0.05],
            "TIME":[dt_time(13, 15), dt_time(13, 20)],
            "LABEL":1,


            "SL":-0.05,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        

        ######################################################### COMENTAR EN LIVE
        self.f3={
            "REGLA":"F3",
            "D":[-0.32,-0.088],
            "DO":[-0.165, 0.05],
            "DCALL":[-0.08 , 0.385],
            "TIME":[dt_time(13, 15), dt_time(13, 20)],
            "LABEL":1,


            "SL":-0.05,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        ######################################################### COMENTAR EN LIVE
        self.f4={
            "REGLA":"F4",
            "D":[-0.23,0.48],
            "DO":[0.14, 0.65],
            "DCALL":[-0.44 , 0.135],
            "TIME":[dt_time(13, 15), dt_time(13, 20)],
            "LABEL":1,


            "SL":-0.05,
            "DIAMANTE":[0.02, 0.025],
            "RESTA":   [0.015 , 0.001]   ,

            "NMT":inf,
            "TARGET_NMT":inf
            }
        
