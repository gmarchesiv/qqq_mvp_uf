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
    def __init__(self):
        ###############################################
        #               PARAMETROS -  GENERALES
        ###############################################

        self.etf = "QQQ"
        self.exchange = ["CBOE"]
        self.zone = pytz.timezone("America/New_York")
        self.fin_rutina = dt_time(15, 55)

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
 

        self.rangos_strikes = [[2, 2.5] ]
        # self.rangos_strikes = [[2, 2.3], [2.15, 2.55], [2.4, 3]]
        self.diff_days_exp = 30
        self.days_max = [30, 45]



        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028

        self.max_askbid_venta_abs = 0.0275
        self.max_askbid_compra_abs = 0.0185

        self.umbral_askbid=0.08
        # self.askbid_len_lista=91

        self.max_askbid_venta_forzada = 0.04

        self.slippage=1.075
        self.fd = dt_time(15, 30)

        self.rutina = [dt_time(7, 0), dt_time(16, 0)]
        self.frecuencia_muestra =[i for i in range(0, 60, 2)]
        self.frecuencia_accion = [i for i in range(0, 60, 2)]
 
        self.intentos=4
        self.tiempo_contulta=5

        #########################################################
        ####################      CALL        ###################
        #########################################################
        # ==================================
        # =========== CALL PROTECCION ======  
        # ==================================
        self.umbral_no_perdida_c = 0.016
        self.perdida_maxima_c = 0.05
        self.perdida_maxima_c_abs = -0.017
        
        # ==================================
        # =========== CALL - R1 ============
        # ==================================
        
        self.dcall_r1 = [0.04, 0.13]
        self.docall_r1 = [0.03, 0.065]
        self.timeCall_r1 = [dt_time(9, 35), dt_time(9, 55)]
        self.labelCall_r1 =0
        
        # VENTA
        self.sl_cr1=-0.05  # STOP LOSS
        # self.min_desicion_cr1  = 60
        self.umbral_manifestacion_cR1=0.0395
        self.diamante_cr1 = [self.umbral_manifestacion_cR1, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_cr1 = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R1-E ========== 
        # ==================================
        
        self.dcall_r1_e = [-0.08, 0.2]
        self.docall_r1_e = [0.05, 0.065]
        self.timeCall_r1_e = [dt_time(10, 20), dt_time(10, 40)]
        self.labelCall_r1_e =0
        
        # VENTA
        self.sl_cr1_e=-0.05  # STOP LOSS
        # self.min_desicion_cr1_e  = 60
        self.umbral_manifestacion_cR1_e=0.0395
        self.diamante_cr1_e = [self.umbral_manifestacion_cR1_e, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R1-FAST =======
        # ==================================
        
        self.dcall_r1_fast = [0.11, 0.25]
        self.docall_r1_fast = [0.13, 0.15]
        self.timeCall_r1_fast = [dt_time(9, 40), dt_time(10, 0)]
        self.labelCall_r1_fast =0
        
        # VENTA
        self.sl_cr1_fast =-0.05  # STOP LOSS
        # self.min_desicion_cr1_fast   = 60
        self.umbral_manifestacion_cR1_fast =0.0395
        self.diamante_cr1_fast  = [self.umbral_manifestacion_cR1_fast , 0.079 ] # DIAMANTE DE COMPRA
        self.resta_cr1_fast  = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =======  CALL - R1 -INV ==========  
        # ==================================
        
        self.dcall_r1_i =[-0.20, 0.05]
        self.docall_r1_i = [0.13, 0.16]
        self.timeCall_r1_i = [dt_time(9, 35), dt_time(10, 0)]
        self.labelCall_r1_i=1
        
        # VENTA
        
        self.sl_cr1_i = -0.05  # STOP LOSS
        self.target_cR1_i=0.03

        

        # ==================================
        # =======  CALL - C       ==========  
        # ==================================
        
        self.dcall_r1_c =[-0.2, 0.25]
        self.docall_r1_c = [0.05, 0.08]
        self.timeCall_r1_c = [dt_time(11, 10), dt_time(12, 40)]
        self.labelCall_r1_c=0
        # VENTA
        self.sl_cr1_c =-0.05  # STOP LOSS
        # self.min_desicion_cr1_c   = 60
        self.umbral_manifestacion_cR1_c =0.0395
        self.diamante_cr1_c = [self.umbral_manifestacion_cR1_c, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_cr1_c= [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R2 ============
        # ==================================

        # COMPRA
        self.dcall_r2 = [0.245, 0.5]
        self.docall_r2 = [0.0445, 0.1]  
        self.timeCall_r2 = [dt_time(9, 35), dt_time(11, 45)]
        self.labelCall_r2=0
        self.umbral_cr2=0.2
        # VENTA
        self.umbral_manifestacion_cR2 =  0.05  # UMBRAL DE MANIFESTACION
        self.sl_cr2 = -0.055  # STOP LOSS
        
        self.diamante_cr2 = [self.umbral_manifestacion_cR2, 0.11, 0.15, 0.2] # DIAMANTE DE COMPRA
        self.resta_cr2 = [0.01, 0.0375, 0.05, 0.001] # RETROCESO DEL DIAMANTE 


        # ==================================
        # =========== CALL - R2-E ==========
        # ==================================

        # COMPRA
        self.dcall_r2_e = [0.5, self.inf]
        self.docall_r2_e = [0.03, 0.075]  
        self.timeCall_r2_e = [dt_time(9, 35), dt_time(10, 45)]
        self.labelCall_r2_e=0
        
        # VENTA
        
        self.sl_cr2 = -0.05  # STOP LOSS
        self.target_cR2_e=0.03


        #########################################################
        ####################      PUT         ###################
        #########################################################

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.016
        self.perdida_maxima_p = 0.05
        self.perdida_maxima_p_abs = -0.017

        # ==================================
        # =========== PUT R1================
        # ==================================
        # COMPRA
        
        self.dput_r1 = [-0.28, 0.21]
        self.doput_r1 = [0.05, 0.065]
        self.timePut_r1 = [dt_time(10, 0), dt_time(10, 20)]
        self.labelPut_r1=1

        # VENTA
        self.sl_pr1=-0.05  # STOP LOSS
        # self.min_desicion_pr1  = 60
        self.umbral_manifestacion_pR1=0.0395
        self.diamante_pr1 = [self.umbral_manifestacion_pR1, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1 = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =======   PUT - R1-INV ==========  
        # ==================================
        
        self.dput_r1_i =[-0.25, 0.03]
        self.doput_r1_i = [0.105, 0.115]
        self.timePut_r1_i = [dt_time(9, 35), dt_time(10,0)]
        self.labelPut_r1_i=0
        
        # VENTA
        self.sl_pr1_i=-0.05  # STOP LOSS
        # self.min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_i=0.0395
        self.diamante_pr1_i = [self.umbral_manifestacion_pR1_i, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1_i = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== PUT R1 E =============
        # ==================================
        # COMPRA
        
        self.dput_r1_e = [-0.25, 0.3]
        self.doput_r1_e = [0.05, 0.09]
        self.timePut_r1_e = [dt_time(10, 15), dt_time(10,35)]
        self.labelPut_r1_e=1

        # VENTA
        self.sl_pr1_e=-0.05  # STOP LOSS
        # self.min_desicion_pr1_e  = 60
        self.umbral_manifestacion_pR1_e=0.0395
        self.diamante_pr1_e = [self.umbral_manifestacion_pR1_e, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1_e = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 


        # ==================================
        # =========== PUT R1-FAST================
        # ==================================
        # COMPRA
        
        self.dput_r1_fast = [-0.02, 0.2]
        self.doput_r1_fast = [0.09, 0.11]
        self.timePut_r1_fast = [dt_time(9, 45), dt_time(9, 55)]
        self.labelPut_r1_fast=1

        # VENTA
        self.sl_pr1_fast=-0.05  # STOP LOSS
        # self.min_desicion_pr1_fast  = 60
        self.umbral_manifestacion_pR1_fast=0.0395
        self.diamante_pr1_fast = [self.umbral_manifestacion_pR1_fast, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1_fast = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 

        
        
        # ==================================
        # =========== PUT R2 ===============
        # ==================================

        # COMPRA
        self.umbral_pr2=0.156
        self.dput_r2 = [0.21, 0.45]  
        self.doput_r2 = [0.055, 0.17]  
        self.timePut_r2 = [dt_time(9, 50), dt_time(10, 30)]
        self.labelPut_r2=1
        self.regreso_do_pr2 = 0.14  # UMBRAL PERMITIDO DEL DOPUT ANTES DE COMPRAR

        # VENTA
        self.umbral_manifestacion_pR2 = 0.03   # UMBRAL DE MANIFESTACION
        self.min_desicion_pr2 = 60  # MINUTOS ANTES DE MANIFESTACION
        self.sl_pr2 = -0.055  # STOP LOSS
        self.diamante_pr2 = [self.umbral_manifestacion_pR2, 0.065,0.09,0.17]  # DIAMANTE DE COMPRA
        self.resta_pr2 = [0.027,0.035,0.035,0.001]  # RETROCESO DEL DIAMANTE

        
        # ==================================
        # =========== PUT R2E ===============
        # ==================================

        # COMPRA
        
        self.dput_r2_e = [0.45, self.inf]  
        self.doput_r2_e = [0.03, 0.075]  
        self.timePut_r2_e = [dt_time(9, 50), dt_time(10, 30)]
        self.labelPut_r2_e=1
        
        # VENTA
        
        self.sl_pr2_e = -0.051  # STOP LOSS
        self.target_pR2_e=0.03


        # ==================================
        # =========== PUT R1 F =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f = [0, self.inf]
        self.doput_r1_f = [0.1, 0.133]
        self.timePut_r1_f = [dt_time(13, 30), dt_time(14, 10)]
        self.labelPut_r1_f=1

        # VENTA
        self.sl_pr1_f=-0.05  # STOP LOSS
        # self.min_desicion_pr1_f  = 60
        self.umbral_manifestacion_pR1_f=0.0395
        self.diamante_pr1_f = [self.umbral_manifestacion_pR1_f, 0.079 ] # DIAMANTE DE COMPRA
        self.resta_pr1_f = [0.01, 0.02 ] # RETROCESO DEL DIAMANTE 



        #########################################################
        ####################      LABELS      ###################
        #########################################################
        
        self.omega=0.00000297000000
        self.alpha=0.027400000
        self.beta=0.90520000
        self.gamma=0.11470000
        self.days_year=252

