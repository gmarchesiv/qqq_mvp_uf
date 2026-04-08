# ====================
#  - Librerias -
# ====================

from datetime import datetime
import time
import holidays
from datetime import time as dt_time

from functions.logs import printStamp
from functions.notifications import sendDisconnection


# ====================
#  - Funciones -
# ====================
 


from datetime import datetime, timedelta

def es_fecha_especial(fecha):
    
    #---------------------------------------------------
    '''
    Analiza los feriados programados y devuelve si es 
    Trading de medio dia , feriado o dia normal.
    '''
    #---------------------------------------------------

    mes, dia = fecha.month, fecha.day
    year = fecha.year

    # ----------- FECHAS FIJAS -----------
    if (mes, dia) == (1, 1):
        return "Año Nuevo", False
    
    if (mes, dia) == (6, 19):
        return "Juneteenth", False

    if (mes, dia) == (7, 4):
        return "4 de julio", False

    if (mes, dia) == (12, 25):
        return "Navidad", False

    if (mes, dia) == (12, 24):
        return "Visperas de Navidad", True

    if (mes, dia) == (7, 3):
        return "3 de julio", True

    # ----------- MLK DAY (3er lunes enero) -----------
    if mes == 1:
        primer_dia = datetime(year, 1, 1)
        primer_lunes = 1 + (7 - primer_dia.weekday()) % 7
        tercer_lunes = primer_lunes + 14
        if dia == tercer_lunes:
            return "Martin Luther King Day", False

    # ----------- PRESIDENTS DAY (3er lunes febrero) -----------
    if mes == 2:
        primer_dia = datetime(year, 2, 1)
        primer_lunes = 1 + (7 - primer_dia.weekday()) % 7
        tercer_lunes = primer_lunes + 14
        if dia == tercer_lunes:
            return "Día de los Presidentes", False

    # ----------- GOOD FRIDAY (variable) -----------
    # Cálculo de Pascua (algoritmo de Meeus)
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    mes_pascua = (h + l - 7*m + 114) // 31
    dia_pascua = ((h + l - 7*m + 114) % 31) + 1

    pascua = datetime(year, mes_pascua, dia_pascua)
    good_friday = pascua - timedelta(days=2)

    if fecha.date() == good_friday.date():
        return "Good Friday", False

    # ----------- MEMORIAL DAY (último lunes mayo) -----------
    if mes == 5:
        ultimo_dia = datetime(year, 5, 31)
        ultimo_lunes = 31 - (ultimo_dia.weekday())
        if dia == ultimo_lunes:
            return "Memorial Day", False

    # ----------- LABOR DAY (primer lunes septiembre) -----------
    if mes == 9:
        primer_dia = datetime(year, 9, 1)
        primer_lunes = 1 + (7 - primer_dia.weekday()) % 7
        if dia == primer_lunes:
            return "Labor Day", False

    # ----------- THANKSGIVING -----------
    if mes == 11:
        primer_dia = datetime(year, 11, 1)
        primer_jueves = 1 + (3 - primer_dia.weekday()) % 7
        cuarto_jueves = primer_jueves + 21

        if dia == cuarto_jueves:
            return "Thanksgiving", False
        elif dia == cuarto_jueves + 1:
            return "Post Thanksgiving", True

    return None, None


def isTradingDay(params):

    # ====================
    #  - Feriados -
    # ====================

    #---------------------------------------------------
    '''
        Revisamos si es Feriado antes de comenzar 
        la rutina, si es el caso no continuara ,
        en caso sea trading day parcial va cambiar 
        el parametro de FD a medio dia.
    '''
    #---------------------------------------------------
    now = datetime.now(params.zone)

    # Llamar a la función con la fecha actual
    resultado, accion = es_fecha_especial(now)

    if resultado:
        if accion:
            printStamp(f"{resultado} - HALF TRADING - ")
            params.fd = dt_time(12, 00)
            params.fin_rutina = dt_time(12, 5)
            return False
        printStamp(f"{resultado} - FERIADO - ")
        return True
    else:
        printStamp(f" - NORMAL TRADING - ")
        return False


def countdown(zone,app,vars,params):

    #---------------------------------------------------
    '''
    Genera una cuenta regresiva (minutos)
    antes de entrar al Trading Day.
    '''
    #---------------------------------------------------
    # ====================
    # - Cuenta Regresiva -
    # ====================

    now = datetime.now(zone)
    start_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

    minuto_ante = 99

    # Bucle de cuenta regresiva

    while True:

        now = datetime.now(zone)

        if now >= start_time and now <= end_time:
            break

        time_diff = start_time - now
        minutes_left = time_diff.total_seconds() // 60

        if minuto_ante != now.minute:
            if (int(minutes_left + 1)) == 1:
                printStamp(f"Faltan {int(minutes_left+1)} minuto para comenzar.")
            else:
                printStamp(f"Faltan {int(minutes_left+1)} minutos para comenzar.")
            minuto_ante = now.minute


        # if now >=  dt_time(7, 30):
        #     if app.alerta==True and vars.flag_alerta==False:
        #         sendDisconnection(params )
        #         vars.flag_alerta=True
        #     if vars.flag_alerta and app.alerta==False :
        #         vars.flag_alerta=False


        time.sleep(1)
