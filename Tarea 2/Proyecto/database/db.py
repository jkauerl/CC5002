import pymysql
import json
import app


with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)

def get_conn():
    conn = pymysql.connect(
    db = 'tarea2',
    user = 'cc5002',
    passwd = 'programacionweb',
    host = 'localhost',
    charset = 'utf8')
    return conn

# Querys

def insertar_donacion(comuna_id, calle_y_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        respuesta = cursor.execute(QUERY_DICT["insertar_donacion"], (comuna_id, calle_y_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular))
        conn.commit()
        donacion_id = cursor.lastrowid
        if respuesta:
            return donacion_id
        else:
            return False
    except pymysql.Error: 
        pass
    return False


def insertar_pedido(comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        respuesta = cursor.execute(QUERY_DICT["insertar_pedido"], (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante))
        conn.commit()
        donacion_id = cursor.lastrowid
        if respuesta:
            return donacion_id
        else:
            return False
    except pymysql.Error: 
        pass
    return False

def insertar_foto(ruta_archivo, nombre_archivo, donacion_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(QUERY_DICT["insertar_foto"], (ruta_archivo, nombre_archivo, donacion_id))
        conn.commit()
    except pymysql.Error: 
        pass
    return False 
	
def lista_donaciones():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["5_1_donaciones"])
    donaciones = cursor.fetchall()
    return donaciones

def lista_pedidos():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["5_1_pedidos"])
    donaciones = cursor.fetchall()
    return donaciones

def obtener_fotos(id_donacion):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["obtener_foto"], id_donacion)
    fotos = cursor.fetchall()
    return fotos

def obtener_info_donacion(id_donacion):
    conn = get_conn()
    cursor=conn.cursor()
    cursor.execute(QUERY_DICT["info_donacion"], id_donacion)
    donacion = cursor.fetchone()
    return donacion

def obtener_info_pedido(id_pedido):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["info_pedido"], id_pedido)
    donacion = cursor.fetchone()
    return donacion