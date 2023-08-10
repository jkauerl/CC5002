from flask import Flask, redirect, render_template, url_for, request, send_from_directory
from validaciones import *
from database import db
import hashlib
from werkzeug.utils import secure_filename
import os
import json

UPLOAD_FOLDER = 'static/uploads'


with open('static/region_comuna.json', 'r') as region_comuna:
	COMUNA_DICT = json.load(region_comuna)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Rutas de la applicacion

@app.route("/") 
def inicio():
    return render_template('inicio.html')

@app.route("/agregar-donacion", methods=('POST', 'GET'))
def agregar_donacion():
    error=0
    if(request.method == "POST"):
        region_id = request.form['region']
        comuna_id = request.form['comuna']
        calle_y_numero = request.form['calle-numero']
        tipo_donacion = request.form['tipo']
        cantidad = request.form['cantidad']
        fecha_disponibilidad = request.form['fecha-disponibilidad']
        descripcion = request.form['descripcion']
        condiciones_retirar = request.form['condiciones']
        foto1 = request.files['foto-1']
        foto2 = request.files['foto-2']
        foto3 = request.files['foto-3']
        nombre = request.form['nombre']
        email = request.form['email']
        celular = request.form['celular']

        if not validador_select(region_id):
            error+=1
        if not validador_select(comuna_id):
            error+=1
        if not validador_largo_max(calle_y_numero, 80):
            error+=1
        if not validador_select(tipo_donacion):
            error+=1
        if not validador_largo_max(cantidad, 250):
            error+=1
        if not validador_fecha(fecha_disponibilidad):
            error+=1
        if not (validador_foto(foto1) or validador_foto(foto2) or validador_foto(foto3)):
            error+=1
        if not (validador_largo_min(nombre, 3) and validador_largo_max(nombre, 80)):
            error+=1
        if not validador_email(email):
            error+=1
        if not validador_celular(celular):
            error+=1

        if not error:
            donacion_id = db.insertar_donacion(comuna_id, calle_y_numero, tipo_donacion, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular)
            
            if foto1: 
                _filename = hashlib.sha256(
                    secure_filename(foto1.filename).encode("utf-8")
                    ).hexdigest()
                _extension = filetype.guess(foto1).extension
                img_filename = f"{_filename}.{_extension}"
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                foto1.save(ruta)
                db.insertar_foto(ruta, img_filename, donacion_id)

            if foto2:
                _filename = hashlib.sha256(
                    secure_filename(foto2.filename).encode("utf-8")
                    ).hexdigest()
                _extension = filetype.guess(foto2).extension
                img_filename = f"{_filename}.{_extension}"
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                foto2.save(ruta)
                db.insertar_foto(ruta, img_filename, donacion_id)
                
            if foto3:
                _filename = hashlib.sha256(
                    secure_filename(foto3.filename).encode("utf-8")
                    ).hexdigest()
                _extension = filetype.guess(foto3).extension
                img_filename = f"{_filename}.{_extension}"
                ruta = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                foto3.save(ruta)
                db.insertar_foto(ruta, img_filename, donacion_id)

            return redirect("/")
        
    
    return render_template("agregar-donacion.html")

@app.route("/agregar-pedido" , methods=('POST', 'GET'))
def agregar_pedido():
    error=0
    if(request.method == "POST"):
        region_id = request.form['region']
        comuna_id = request.form['comuna']
        tipo_pedido = request.form['tipo']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        nombre = request.form['nombre']
        email = request.form['email']
        celular = request.form['celular']

        if not validador_select(region_id):
            error+=1
        if not validador_select(comuna_id):
            error+=1
        if not validador_select(tipo_pedido):
            error+=1
        if not validador_largo_max(descripcion, 250):
            error+=1
        if not validador_largo_max(cantidad, 250):
            error+=1
        if not (validador_largo_min(nombre, 3) and validador_largo_max(nombre, 80)):
            error+=1
        if not validador_email(email):
            error+=1
        if not validador_celular(celular):
            error+=1

        if not error:
            db.insertar_pedido(comuna_id, tipo_pedido, descripcion, cantidad, nombre, email, celular)
            return redirect("/")
    return render_template("agregar-pedido.html")

@app.route("/ver-donaciones/")
@app.route("/ver-donaciones/<int:inicio>")
def ver_donaciones(inicio=0):

    donaciones = []
    for donacion in db.lista_donaciones():
        id_donacion, comuna_id, calle_numero, tipo, cantidad, fecha, descripcion, condiciones_retirar, nombre, email, celular = donacion
        fotos = []
        for foto in db.obtener_fotos(id_donacion):
            id_foto, ruta_archivo, nombre_archivo, donacion_id = foto
            nombre_archivo = f"uploads/{nombre_archivo}"
            url = url_for('static', filename=nombre_archivo)
            fotos.append(url) 

        comuna = None 
        for region in COMUNA_DICT['regiones']:
            comunas = region['comunas']
            for c in comunas:
                if c['id'] == comuna_id:
                    comuna = c['nombre']
                    break
            if comuna:
                break 

        donaciones.append({
            "id": id_donacion,
            "comuna": comuna,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha_disponibilidad": fecha,
            "nombre": nombre,
            "url": fotos
        }) 
    print(donaciones[1])
    fin = inicio + 5
    donaciones_pagina = donaciones[inicio:fin]

    hay_siguiente = False
    if fin < len(donaciones):
        hay_siguiente = True
    hay_anterior = False
    if inicio > 0: 
        hay_anterior = True

    return render_template("ver-donaciones.html", donaciones_pagina=donaciones_pagina, inicio=inicio, hay_siguiente=hay_siguiente, hay_anterior=hay_anterior)


@app.route("/ver-pedidos/")
@app.route("/ver-pedidos/<int:inicio>")
def ver_pedidos(inicio=0):

    pedidos = []
    for pedido in db.lista_pedidos():
        id, comuna_id, tipo, descripcion, cantidad, nombre, email_solicitante, celular_solicitante = pedido

        comuna = None
        for region in COMUNA_DICT['regiones']:
            comunas = region['comunas']
            for c in comunas:
                if c['id'] == comuna_id:
                    comuna = c['nombre']
                    break
            if comuna:
                break

        pedidos.append({
            "id": id,
            "comuna": comuna,
            "descripcion": descripcion,
            "tipo": tipo, 
            "cantidad": cantidad,
            "nombre": nombre,      
        })

    fin = inicio + 5
    pedidos_pagina = pedidos[inicio:fin]

    hay_siguiente = False
    if fin < len(pedidos):
        hay_siguiente = True
    hay_anterior = False
    if inicio > 0:
        hay_anterior = True

    return render_template('ver-pedidos.html', pedidos_pagina=pedidos_pagina, inicio=inicio, hay_siguiente=hay_siguiente, hay_anterior=hay_anterior)



@app.route("/informacion-donacion/<id>")
def informacion_donacion(id):
    
    donacion_db = db.obtener_info_donacion(id)
    id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular = donacion_db

    fotos = []
    for foto in db.obtener_fotos(id):
        id_foto, ruta_archivo, nombre_archivo, donacion_id = foto
        nombre_archivo = f"uploads/{nombre_archivo}"
        url = url_for('static', filename=nombre_archivo)
        fotos.append(url) 

    comuna = None
    region = None

    for reg in COMUNA_DICT['regiones']:
        comunas = reg['comunas']
        for com in comunas:
            if com['id'] == comuna_id:
                comuna = com['nombre']
                region = reg['nombre']
                break
        if comuna:
            break

    donacion = {
        "region": region,
        "comuna": comuna,
        "calle": calle_numero,
        "tipo": tipo,
        "cantidad": cantidad,
        "fecha": fecha_disponibilidad,
        "descripcion": descripcion,
        "condicion": condiciones_retirar,
        "foto": fotos,
        "nombre": nombre,
        "email": email,
        "celular": celular
    }

    return render_template("informacion-donacion.html", donacion=donacion)


@app.route("/informacion-pedido/<id>")
def informacion_pedido(id): 
    
    pedido_db = db.obtener_info_pedido(id)
    id, comuna_id, tipo, descripcion, cantidad, nombre, email, celular = pedido_db

    comuna = None
    region = None

    for reg in COMUNA_DICT['regiones']:
        comunas = reg['comunas']
        for com in comunas:
            if com['id'] == comuna_id:
                comuna = com['nombre']
                region = reg['nombre']
                break
        if comuna:
            break

    pedido = {
        "region": region,
        "comuna": comuna,
        "tipo": tipo,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "nombre": nombre,
        "email": email,
        "celular": celular
    }

    return render_template("informacion-pedido.html", pedido=pedido)

if __name__ == "__main__":
    app.run(debug=True)