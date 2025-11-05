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
 

        self.rangos_strikes = [[2, 2.5] ]
        # self.rangos_strikes = [[2, 2.3], [2.15, 2.55], [2.4, 3]]
        self.diff_days_exp = 30
        self.days_min_exp = 25  # DIAS para el exp minimo de busqueda


        self.days_max = [30, 45]



        self.max_askbid_venta_prom = 0.03
        self.max_askbid_compra_prom = 0.028

        self.max_askbid_venta_abs = 0.0275
        self.max_askbid_compra_abs = 0.0185
        self.days_min_exp = 25  # DIAS para el exp minimo de busqueda
        self.umbral_askbid=0.08
        self.max_askbid_open = 0.03
        self.max_askbid_hora_open =  dt_time(9, 33)
        # self.askbid_len_lista=91

        self.max_askbid_venta_forzada = 0.04

        self.slippage=1.06
        self.fd = dt_time(15, 30)

        self.rutina = [dt_time(6, 50), dt_time(16, 0)]
        self.frecuencia_muestra =[i for i in range(0, 60, 2)]
        self.frecuencia_accion = [i for i in range(0, 60, 2)]
 
        self.intentos=1
        self.tiempo_contulta=5
        self.proteccion_ask_bid=[[dt_time(9, 45,0), dt_time(9, 45,18)],[dt_time(10, 0,0), dt_time(10,0,18 )]]


        self.proteccion_compra=[ dt_time(9, 44,0), dt_time(9, 45,30) ]
        self.proteccion_compra_2=[ dt_time(9, 59,0), dt_time(10, 0,15) ]
        self.proteccion_compra_call_r1=[ dt_time(9, 44,0), dt_time(9, 46,0)  ]
        ##########################################
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
        self.perdida_maxima_c_r2 = 0.04
        # ==================================
        # =========== CALL - R1 ============
        # ==================================
        
        self.dcall_r1 = [0.09, 0.133]
        self.docall_r1 = [0.03, 0.05]
        self.timeCall_r1 = [dt_time(9, 35), dt_time(9, 56)]
        self.labelCall_r1 =0
        
        # VENTA
    
        # self.min_desicion_cr1  = 60
        self.sl_cr1 = -0.035  # STOP LOSS

        # self.target_cR1=0.04
        self.umbral_manifestacion_cR1 = 0 
        self.diamante_cr1 = [self.umbral_manifestacion_cR1  ,0.04  ] # DIAMANTE DE COMPRA
        self.resta_cr1  = [ 0.038  , self.inf_n] # RETROCESO DEL DIAMANTE 



        # ==================================
        # =========== CALL - R1-E ==========  
        # ==================================
        
        self.dcall_r1_e = [-0.155, 0.077 ]
        self.docall_r1_e = [0.059, 0.065]
        self.timeCall_r1_e = [dt_time(10,14), dt_time(10, 16)]
        self.labelCall_r1_e =0
        
        # VENTA
        self.sl_cr1_e=-0.048  # STOP LOSS
        # min_desicion_cr1_e  = 60
        self.umbral_manifestacion_cR1_e= 0.0285
        self.diamante_cr1_e = [self.umbral_manifestacion_cR1_e,0.0379, 0.07 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e = [0.0276,0.01, self.inf_n ] # RETROCESO DEL DIAMANTE 

        self.bloqueo_cr1_e_docall=0.15
        self.bloqueo_cr1_e_doput=0.06
        # bloqueo_cr1_e_dput= -0.05
        self.bloqueo_cr1_e_hora=dt_time(10,0)
        # ==================================
        # =========== CALL - R1-E2 ==========  
        # ==================================
        
        self.dcall_r1_e2 =  [-0.155, 0.1 ]
        self.docall_r1_e2 =[0.057, 0.0631]
        self.timeCall_r1_e2 = [dt_time(10,26), dt_time(10, 40)]
        self.labelCall_r1_e2 =0
        
        # VENTA
        self.sl_cr1_e2=-0.04  # STOP LOSS
        # min_desicion_cr1_e2  = 60
        self.umbral_manifestacion_cR1_e2= 0.0255
        self.diamante_cr1_e2 = [self.umbral_manifestacion_cR1_e2,0.0379, 0.07 ] # DIAMANTE DE COMPRA
        self.resta_cr1_e2 = [0.02,0.01, self.inf_n ] # RETROCESO DEL DIAMANTE 
    

        # ==================================
        # =======  CALL - R1 -INV ==========  
        # ==================================
        
        self.dcall_r1_i =[-0.37, 0]
        self.docall_r1_i =[0.1, 0.105]
        self.timeCall_r1_i = [dt_time(9, 35), dt_time(9,55)]
        self.labelCall_r1_i=1
        self.dcall_r1_i_dput=0.26
        
        # VENTA
        
        self.sl_cr1_i = -0.048  # STOP LOSS
        self.target_cR1_i=0.03

        

        # ==================================
        # =======  CALL - C       ==========  
        # ==================================
        
        self.dcall_r1_c =[-0.17,-0.04]
        self.docall_r1_c = [0.1, 0.11]
        self.timeCall_r1_c = [dt_time(11, 30), dt_time(12, 15)]
        self.labelCall_r1_c=0
        # VENTA
        self.sl_cr1_c =-0.04  # STOP LOSS
        # min_desicion_cr1_c   = 60
        self.umbral_manifestacion_cR1_c =0.0198
        self.diamante_cr1_c = [self.umbral_manifestacion_cR1_c,0.0379, 0.078,0.15 ] # DIAMANTE DE COMPRA
        self.resta_cr1_c= [0.015,0.01,0.02, self.inf_n ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== CALL - R2 ============
        # ==================================

        # COMPRA
        self.dcall_r2 = [0.27, 0.425]
        self.docall_r2 = [0.032, 0.055]  
        self.timeCall_r2 = [dt_time(9, 35), dt_time(10, 45)]
        self.labelCall_r2=0
        self.umbral_cr2=0.225
        # VENTA
        # self.umbral_manifestacion_cR2 =  0.05  # UMBRAL DE MANIFESTACION
        self.min_desicion_cR2   = 60
 
        
        self.target_min_desicion_cR2 =0.01
        self.sl_cr2 = -0.05  # STOP LOSS
        self.umbral_manifestacion_cR2=0.025
        self.diamante_cr2 = [self.umbral_manifestacion_cR2  ,0.035 ] # DIAMANTE DE COMPRA
        self.resta_cr2= [0.0225,0.005] # RETROCESO DEL DIAMANTE 
        # self.target_cR2=0.11


        # ==================================
        # =========== CALL - R1-FAST =======
        # ==================================
        
        self.dcall_r1_fast = [-0.02 ,0.08]
        self.docall_r1_fast =  [0.04, 0.057]
        self.timeCall_r1_fast = [dt_time(9, 35), dt_time(9, 55)]
        self.labelCall_r1_fast =0
        
        # VENTA
        self.sl_cr1_fast =-0.045  # STOP LOSS
        # min_desicion_cr1_fast   = 60
        self.umbral_manifestacion_cR1_fast =0.02 
        self.diamante_cr1_fast  = [self.umbral_manifestacion_cR1_fast , 0.028   ] # DIAMANTE DE COMPRA
        self.resta_cr1_fast  = [0.015,0.005  ]# RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== CALL - R3 =======
        # ==================================
        
        self.dcall_r3 =  [ 0.2, 0.225]
        self.docall_r3 =  [0.03, 0.04]
        self.timeCall_r3 =  [dt_time(9, 38), dt_time(9, 45)]
        self.labelCall_r3=0
        
        # VENTA
        self.sl_cr3 =-0.046  # STOP LOSS
        
        self.umbral_manifestacion_cR3 =0.024
        self.diamante_cr3  = [  self.umbral_manifestacion_cR3, 0.031  ] # DIAMANTE DE COMPRA
        self.resta_cr3  = [  0.02,self.inf_n]# RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== CALL R1 F1 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f1 = [-0.22,-0.08]
        self.docall_r1_f1 = [0.095, 0.11]
        self.timecall_r1_f1 = [dt_time(12, 30), dt_time(12, 32)]
        self.labelcall_r1_f1=0

        # VENTA
        self.sl_cr1_f1=-0.04  # STOP LOSS
    

        self.umbral_manifestacion_cR1_f1=0.0285
        self.diamante_cr1_f1 = [
        self.umbral_manifestacion_cR1_f1,
        0.04
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f1 = [0.02, self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== CALL R1 F2 =============
        # ==================================
        # COMPRA
        
        self.dcall_r1_f2 = [0.25, 0.35]
        self.docall_r1_f2 = [0.095, 0.11]
        self.timecall_r1_f2 = [dt_time(12, 30), dt_time(12, 32)]
        self.labelcall_r1_f2=0

        # VENTA
        self.sl_cr1_f2=-0.04  # STOP LOSS
        # self.min_desicion_pr1_f2  = 60
        # self.target_pR1_f2 =0.04

        self.umbral_manifestacion_cR1_f2=0.0235
        self.diamante_cr1_f2 = [
        self.umbral_manifestacion_cR1_f2,
        0.03
        ]  # DIAMANTE DE COMPRA
        self.resta_cr1_f2 = [0.0295, self.inf_n]   # RETROCESO DEL DIAMANTE

     
        #########################################################
        ####################      PUT         ###################
        #########################################################

        # ==================================
        # =========== PUT PROTECCION ======= 
        # ==================================

        self.umbral_no_perdida_p = 0.015
        
        self.perdida_maxima_p = 0.045
    
        self.perdida_maxima_p_abs = -0.017

        self.umbral_no_perdida_p_r2 = 0.016
        self.perdida_maxima_p_r2 = 0.04
        # ==================================
        # =========== PUT R1================
        # ==================================
        # COMPRA
        
        self.dput_r1 = [-0.23, -0.04]
        self.doput_r1 = [0.057, 0.065]
        self.timePut_r1 = [dt_time(10, 0), dt_time(10, 20)]
        self.labelPut_r1=1

        # VENTA
        
        self.sl_pr1 = -0.035  # STOP LOSS
        self.umbral_manifestacion_pR1= 0.029
        self.diamante_pr1  = [self.umbral_manifestacion_pR1 ,0.0385 ] # DIAMANTE DE COMPRA
        self.resta_pr1  = [0.015 ,self.inf_n ] # RETROCESO DEL DIAMANTE 
        
        

        # ==================================
        # =======   PUT - R1-INV ==========  
        # ==================================
        
        self.dput_r1_i =[-0.19, -0.01]
        self.doput_r1_i = [0.105, 0.11]
        self.timePut_r1_i = [dt_time(9, 35), dt_time(9,55)]
        self.labelPut_r1_i=0
        
        # VENTA
        self.sl_pr1_i=-0.048  # STOP LOSS
        # min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_i=0.023
        self.diamante_pr1_i = [self.umbral_manifestacion_pR1_i ,0.0379,0.07] # DIAMANTE DE COMPRA
        self.resta_pr1_i = [0.045, 0.01 ,0.005 ] # RETROCESO DEL DIAMANTE 
        # self.target_pR1_i=0.08


        # ==================================
        # =======   PUT - R1-INV 2==========  
        # ==================================
        
        self.dput_r1_i_2 =[-0.29, -0.089]
        self.doput_r1_i_2 = [0.095, 0.105]
        self.timePut_r1_i_2 = [dt_time(10,30), dt_time(11,10)]
        self.labelPut_r1_i_2=0
        
        # VENTA
        self.sl_pr1_i_2=-0.045  # STOP LOSS
        # min_desicion_pr1_i  = 60
        self.umbral_manifestacion_pR1_i_2=0.023
        self.diamante_pr1_i_2 = [self.umbral_manifestacion_pR1_i_2 ,0.0295 ]# DIAMANTE DE COMPRA
        self.resta_pr1_i_2 =  [0.04 , self.inf_n ] # RETROCESO DEL DIAMANTE 
        
        # ==================================
        # =======   PUT - R1-INV 3==========  
        # ==================================
        
        self.dput_r1_i_3 =[0.053, 0.1]
        self.doput_r1_i_3 = [0.1, 0.11]
        self.timePut_r1_i_3 = [dt_time(9,50), dt_time(10,5)]
        self.labelPut_r1_i_3=0
        
        # VENTA
        self.sl_pr1_i_3=-0.045  # STOP LOSS
        # min_desicion_pr1_i_3  = 60
        self.umbral_manifestacion_pR1_i_3=0.023
        self.diamante_pr1_i_3 = [self.umbral_manifestacion_pR1_i_3 ,0.0295 ]# DIAMANTE DE COMPRA
        self.resta_pr1_i_3 =  [0.04 , self.inf_n ] # RETROCESO DEL DIAMANTE 
        
        # ==================================
        # =======   PUT - R1-E ==========   COMENTADA
        # ==================================
        
        self.dput_r1_e =[-0.03, 0.085]
        self.doput_r1_e = [0.05, 0.09]
        self.timePut_r1_e = [dt_time(10, 30), dt_time(11,0)]
        self.labelPut_r1_e=0
        
        # VENTA
        self.sl_pr1_e=-0.05  # STOP LOSS
        # min_desicion_pr1_e  = 60
        self.umbral_manifestacion_pR1_e=0.0379
        self.diamante_pr1_e = [self.umbral_manifestacion_pR1_e ,0.078] # DIAMANTE DE COMPRA
        self.resta_pr1_e = [ 0.01 ,self.inf_n ] # RETROCESO DEL DIAMANTE 
        self.target_pR1_e=0.08

        


        # ==================================
        # =========== PUT R1-FAST================
        # ==================================
        # COMPRA
        
        self.dput_r1_fast = [ 0.0755, 0.155]
        self.doput_r1_fast = [0.0805, 0.0885]
        self.timePut_r1_fast = [dt_time(9, 40), dt_time(9, 55)]
        self.labelPut_r1_fast=1

        # VENTA
        self.sl_pr1_fast=-0.045  # STOP LOSS
        # min_desicion_pr1_fast  = 60
        self.umbral_manifestacion_pR1_fast=0.028
        self.diamante_pr1_fast = [self.umbral_manifestacion_pR1_fast, 0.0379 ,0.08] # DIAMANTE DE COMPRA
        self.resta_pr1_fast = [0.01,0.01 ,self.inf_n ] # RETROCESO DEL DIAMANTE 
    
        # ==================================
        # =========== PUT Label================
        # ==================================
        # COMPRA
        
        self.dput_r1_label = [ -0.06, 0.1]
        self.doput_r1_label = [0.054, 0.06]
        self.timePut_r1_label = [dt_time(10, 5), dt_time(10, 35)]
        self.labelPut_r1_label=1

        # VENTA
        self.sl_pr1_label=-0.045  # STOP LOSS
        # min_desicion_pr1_label  = 60
        self.umbral_manifestacion_pR1_label=0.028
        self.diamante_pr1_label= [self.umbral_manifestacion_pR1_label, 0.0379 ,0.08] # DIAMANTE DE COMPRA
        self.resta_pr1_label = [0.01,0.01 ,self.inf_n ] # RETROCESO DEL DIAMANTE 

        # ==================================
        # =========== PUT R2 ===============
        # ==================================

        # COMPRA
        self.umbral_pr2=0.15
        self.dput_r2 = [0.21, 0.33]  
        self.doput_r2 = [0.055, 0.071]  
        self.timePut_r2 = [dt_time(9, 43), dt_time(9, 55)]
        self.labelPut_r2=1
        self.regreso_do_pr2 = 0.14  # UMBRAL PERMITIDO DEL DOPUT ANTES DE COMPRAR

        # VENTA
    
        # min_desicion_pr2 = 60  # MINUTOS ANTES DE MANIFESTACION
        self.sl_pr2 = -0.045  # STOP LOSS
        self.umbral_manifestacion_pR2=0.0285
        self.diamante_pr2 = [
        self.umbral_manifestacion_pR2,
        0.0379,
        0.06
        ]  # DIAMANTE DE COMPRA
        self.resta_pr2 = [0.02 ,0.01,self.inf_n]   # RETROCESO DEL DIAMANTE
        self.target_pR2 =0.11
        
        # ==================================
        # =========== PUT R2E ===============
        # ==================================

        # COMPRA
        
        self.dput_r2_e = [0.385, 0.57]  
        self.doput_r2_e = [0.0355, 0.073]  
        self.timePut_r2_e = [dt_time(9, 50), dt_time(9, 55)]
        self.labelPut_r2_e=1
        
        # VENTA
        
        self.sl_pr2_e = -0.045  # STOP LOSS
        self.target_pR2_e=0.026


        # ==================================
        # =========== PUT R1 C ============= COMENTADA
        # ==================================
        # COMPRA
        
        self.dput_r1_c = [self.inf_n,self.inf]
        self.doput_r1_c = [0.1, 0.11]
        self.timePut_r1_c = [dt_time(10, 5), dt_time(11, 30)]
        self.labelPut_r1_c=1

        # VENTA
        self.sl_pr1_c=-0.05  # STOP LOSS
        # min_desicion_pr1_c  = 60
        # self.target_pR1_c =0.04

        self.umbral_manifestacion_pR1_c=0.0379
        self.diamante_pr1_c = [
        self.umbral_manifestacion_pR1_c,0.078]  # DIAMANTE DE COMPRA
        self.resta_pr1_c = [0.01, self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== PUT R1 F =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f = [0, 0.2]
        self.doput_r1_f = [0.08, 0.115]
        self.timePut_r1_f = [dt_time(13, 30), dt_time(14, 10)]
        self.labelPut_r1_f=1

        # VENTA
        self.sl_pr1_f=-0.035  # STOP LOSS
        # min_desicion_pr1_f  = 60
        # self.target_pR1_f =0.04

        self.umbral_manifestacion_pR1_f=0.0285
        self.diamante_pr1_f = [
        self.umbral_manifestacion_pR1_f,
        0.04
        ]  # DIAMANTE DE COMPRA
        self.resta_pr1_f = [0.02 , self.inf_n]   # RETROCESO DEL DIAMANTE


        # ==================================
        # =========== PUT R1 F2 =============
        # ==================================
        # COMPRA
        
        self.dput_r1_f2 = [0.07, 0.18]
        self.doput_r1_f2 = [0.08, 0.115]
        self.timePut_r1_f2 = [dt_time(14, 45), dt_time(15, 5)]
        self.labelPut_r1_f2=1

        # VENTA
        self.sl_pr1_f2=-0.035  # STOP LOSS
        # min_desicion_pr1_f  = 60
        # self.target_pR1_f =0.04

        self.umbral_manifestacion_pR1_f2=0.023
        self.diamante_pr1_f2 = [
        self.umbral_manifestacion_pR1_f2 ,0.03
        ]  # DIAMANTE DE COMPRA
        self.resta_pr1_f2 = [0.02 ,  self.inf_n]   # RETROCESO DEL DIAMANTE

        # ==================================
        # =========== PUT R3 ===============
        # ==================================
        # COMPRA
        
        self.dput_r3 = [ 0.16, 0.19]
        self.doput_r3 = [0.0485, 0.065]
        self.timePut_r3 = [dt_time(9, 55), dt_time(10, 15)]
        self.labelPut_r3=1

        # VENTA
        
        self.sl_pr3 = -0.035   # STOP LOSS
        self.umbral_manifestacion_pR3=0.023
        self.diamante_pr3  = [self.umbral_manifestacion_pR3 ,0.04  ] # DIAMANTE DE COMPRA
        self.resta_pr3  = [ 0.02 , self.inf_n]
    



        #########################################################
        ####################      LABELS      ###################
        #########################################################
        
        self.omega=0.00000297000000
        self.alpha=0.027400000
        self.beta=0.90520000
        self.gamma=0.11470000
        self.days_year=252

