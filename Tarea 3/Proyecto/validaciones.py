import re
from datetime import datetime
import filetype

# Funciones basicas que validan la existencia y ciertas condciones

def validador_largo_max(texto, largo):
    return bool(texto) and len(texto) <= largo

def validador_largo_min(texto, largo):
    return bool(texto) and len(texto) >= largo

def validador_email(mail):
    return bool(mail) and "@" in mail and validador_largo_min(mail, 5)

def validador_fecha(fecha):
    fecha_arr = fecha.split("-")
    if (
        len(fecha_arr) == 3
        and len(fecha_arr[0]) == 4
        and len(fecha_arr[1]) == 2
        and len(fecha_arr[2]) == 2
    ):
        dia_actual = datetime.now()
        dia_ingresado = datetime(
            int(fecha_arr[0]), int(fecha_arr[1]), int(fecha_arr[2])
        )
        if dia_ingresado >= dia_actual:
            return True
        else:
            return False
    else:
        return False

def validador_select(select):
    if select == "":
        return False
    else:
        return True

def validador_celular(numero):
    patron_celular_chile = r"^(?:\+?56|0)[2-9]\d{1}\s?\d{3}\s?\d{4}$"
    return bool(re.match(patron_celular_chile, numero))


def validador_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if foto is None:
        return False

    # check if the browser submitted an empty file
    if foto.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def hay_comuna_en_region(comuna_name, region_name, data):
    for region in data["regiones"]:
        if region["nombre"] == region_name:
            for comuna in region["comunas"]:
                if comuna["nombre"] == comuna_name:
                    return True
            return False
    return False

def hay_region_en_comuna(region_name, comuna_name, data):
    for region in data["regiones"]:
        if region["nombre"] == region_name:
            for comuna in region["comunas"]:
                if comuna["nombre"] == comuna_name:
                    return True
            return False
    return False