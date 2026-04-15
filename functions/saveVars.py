# ====================
#  - Librerias -
# ====================
from datetime import datetime
import json
import os
import pytz
from collections import deque

# =======================
#  - GUARDAR VAIRBALES -
# =======================
def saveVars(vars, app, params, estado):
    file_name = "/usr/src/app/data/vars.json"
    now = datetime.now(params.zone)
    
    vars.name=params.name
    vars.wallet=app.wallet
    vars.date= now.date().isoformat() 
    vars.time= now.time().isoformat() 
    vars.trade_hour= str(vars.trade_hour)
    if estado:

        vars.call_dic = {
            "ask": 0,
            "bid": 0,
            "askSize": 0,
            "bidSize": 0,
            "symbol": "",
            "strike": "",
        }
        vars.put_dic = {
            "ask": 0,
            "bid": 0,
            "askSize": 0,
            "bidSize": 0,
            "symbol": "",
            "strike": "",
        }
        vars.price = 0
    else:

        vars.call_dic = {
            "ask": vars.cask,
            "bid": vars.cbid,
            "askSize": app.options[1]["ASK_SIZE"],
            "bidSize": app.options[1]["BID_SIZE"],
            "symbol": app.options[1]["symbol"],
            "strike": app.options[1]["strike"],
        }
        vars.put_dic = {
            "ask": vars.pask,
            "bid": vars.pbid,
            "askSize": app.options[2]["ASK_SIZE"],
            "bidSize": app.options[2]["BID_SIZE"],
            "symbol": app.options[2]["symbol"],
            "strike": app.options[2]["strike"],
        }

        vars.price = app.etfs[5]["price"]
    # data = vars.__dict__.copy()
    # data["askbid_call_prom"]=list(vars.askbid_call_prom)
    # data["askbid_put_prom"]=list(vars.askbid_put_prom)
    vars.askbid_call_prom=list(vars.askbid_call_prom)
    vars.askbid_put_prom=list(vars.askbid_put_prom)
    with open(file_name, "w") as json_file:
        json.dump(vars.__dict__, json_file, indent=4)
    vars.askbid_call_prom=deque(vars.askbid_call_prom, maxlen=89)
    vars.askbid_put_prom=deque(vars.askbid_put_prom, maxlen=89)
    

 

async def saveApp(varsApp, app,  params  ):
    #---------------------------------------------------
    '''
    Guardado de los datos en json.
    '''
    #---------------------------------------------------
    file_name = "/usr/src/app/data/app.json"
    now = datetime.now(params.zone)
  
    
    datos = {
        "cash": app.cash,
        "statusIB": app.statusIB,
        "execution_details": app.execution_details,
        "commissions": app.commissions,
        "sendError": app.sendError,
        "Error": app.Error,
        "Error_buy": app.Error_buy 
        
    }

    with open(file_name, "w") as json_file:
        json.dump(datos, json_file, indent=4)



async def saveLabel(varsLb):
    file_name = "/usr/src/app/data/label.json"
    datos_lb = {
        ###############################################
        # LABEL
        ###############################################
        "flag_minuto_label": varsLb.flag_minuto_label,
        "label": int(varsLb.label),
        "retorno": varsLb.retorno,
        "signo": varsLb.signo,
        "varianza": varsLb.varianza,
        "pico_etf": varsLb.pico_etf,
        "d_pico": varsLb.d_pico,
        "rsi": varsLb.rsi,
        "mu": varsLb.mu,
        "mu_conteo": varsLb.mu_conteo ,

        # Listas y Deques
        "retorno_lista":[float(x) for x in varsLb.retorno_lista],
        "ret_1H_back":[float(x) for x in varsLb.ret_1H_back],
        "ret_3H_back": [float(x) for x in varsLb.ret_3H_back],
        "ret_6H_back": [float(x) for x in varsLb.ret_6H_back],
        "ret_12H_back":[float(x) for x in varsLb.ret_12H_back],
        "ret_24H_back": [float(x) for x in varsLb.ret_24H_back],
        "ret_96H_back": [float(x) for x in varsLb.ret_96H_back],
        "etf_price_lista":[float(x) for x in varsLb.etf_price_lista]
    
    }
    with open(file_name, "w") as json_file:
        json.dump(datos_lb, json_file, indent=4)
