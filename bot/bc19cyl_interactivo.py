#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import operator
import os
import re
from datetime import datetime, timedelta
import pymongo
import telebot
import urllib3
from telebot import types
import logrm
import time


# Request to API data
def requestAPI(argurl):
    try:
        response = http.request('GET', url=argurl)
        if response.status != 200:
            data_json = {"ok": False, "error_code": response.status, "description": response.data.decode('utf-8')}
        else:
            data_json = json.loads(response.data.decode('utf-8'))
        return data_json

    except Exception as e2:
        data_json = {"ok": False, "description": str(e2)}
        return data_json


# Envia keyboard principal
def ky_general():
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton('Casos confirmados COVID-19', callback_data="g1")
    bt02 = types.InlineKeyboardButton('Posibles casos COVID-19', callback_data="g2")
    bt09 = types.InlineKeyboardButton('Vacunaciones', callback_data="g10")
    bt03 = types.InlineKeyboardButton('Situación actual en hospitales', callback_data="g3")
    bt04 = types.InlineKeyboardButton('Ocupación hospitalaria', callback_data="g4")
    bt05 = types.InlineKeyboardButton('Test y pruebas', callback_data="g5")
    bt06 = types.InlineKeyboardButton('Mortalidad', callback_data="g6")
    # bt07 = types.InlineKeyboardButton('Fase de Desescalada', callback_data="g8")
    bt07 = types.InlineKeyboardButton('Indicadores de Riesgo', callback_data="g9")
    bt08 = types.InlineKeyboardButton('Ajustes', callback_data="g7")
    markup.row(bt09)
    markup.row(bt01)
    markup.row(bt02)
    markup.row(bt03)
    markup.row(bt04)
    markup.row(bt05)
    markup.row(bt06)
    markup.row(bt07)
    markup.row(bt08)
    return markup


# Envia keyboard ciudades
def kyciudades(pre):
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton('Ávila', callback_data="{0}_av".format(pre))
    bt02 = types.InlineKeyboardButton('Burgos', callback_data="{0}_bu".format(pre))
    bt03 = types.InlineKeyboardButton('León', callback_data="{0}_le".format(pre))
    bt04 = types.InlineKeyboardButton('Palencia', callback_data="{0}_pa".format(pre))
    bt05 = types.InlineKeyboardButton('Salamanca', callback_data="{0}_sa".format(pre))
    bt06 = types.InlineKeyboardButton('Segovia', callback_data="{0}_se".format(pre))
    bt07 = types.InlineKeyboardButton('Soria', callback_data="{0}_so".format(pre))
    bt08 = types.InlineKeyboardButton('Valladolid', callback_data="{0}_va".format(pre))
    bt09 = types.InlineKeyboardButton('Zamora', callback_data="{0}_za".format(pre))
    markup.row(bt01, bt02, bt03)
    markup.row(bt04, bt05, bt06)
    markup.row(bt07, bt08, bt09)
    return markup


# Teclado Gerencias
def kygerencias(pre):
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton('Ávila', callback_data="{0}_av".format(pre))
    bt02 = types.InlineKeyboardButton('Burgos', callback_data="{0}_bu".format(pre))
    bt03 = types.InlineKeyboardButton('León', callback_data="{0}_le".format(pre))
    bt04 = types.InlineKeyboardButton('Palencia', callback_data="{0}_pa".format(pre))
    bt05 = types.InlineKeyboardButton('Ponferrada', callback_data="{0}_po".format(pre))
    bt06 = types.InlineKeyboardButton('Salamanca', callback_data="{0}_sa".format(pre))
    bt07 = types.InlineKeyboardButton('Segovia', callback_data="{0}_se".format(pre))
    bt08 = types.InlineKeyboardButton('Soria', callback_data="{0}_so".format(pre))
    bt09 = types.InlineKeyboardButton('Valladolid Este', callback_data="{0}_vae".format(pre))
    bt10 = types.InlineKeyboardButton('Valladolid Oste', callback_data="{0}_vao".format(pre))
    bt11 = types.InlineKeyboardButton('Zamora', callback_data="{0}_za".format(pre))
    markup.row(bt01, bt02, bt03)
    markup.row(bt04, bt05, bt06)
    markup.row(bt07, bt08, bt09)
    markup.row(bt10, bt11)
    return markup


# Teclado volver para atras
def kyvolver(pre, texto):
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton(texto, callback_data=pre)
    bt02 = types.InlineKeyboardButton('Menú principal', callback_data="menuprincipal")
    markup.row(bt01)
    markup.row(bt02)
    return markup


# Teclado ajustes
def kyajustes():
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton('Activar', callback_data="activarnotificacion")
    bt02 = types.InlineKeyboardButton('Desactivar', callback_data="desactivarnotificacion")
    markup.row(bt01, bt02)
    return markup


# Agregamos usuario a la db
def checkUser(userdoc):
    try:
        userdoc2 = userColl.find_one({"_id": userdoc['_id']})
        if userdoc2 is None:
            logger.info("New user: {0}".format(userdoc))
            userColl.insert_one(userdoc)

    except Exception as e:
        logger.error("Error al guardar usuario nuevo en db {0}. {1}".format(userdoc, e))


# Guardamos historial
def dbhistorial(message, typemessage):
    try:
        id_user = message.from_user.id
        name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        last_access = datetime.utcnow()

        user_document = {
            '_id': str(id_user),
            'username': username,
            'name': name,
            'lastName': last_name,
            'lastAccess': last_access
        }

        userColl.update_one({"_id": str(id_user)},
                            {"$set": user_document}, upsert=True)

        msj = ""
        if typemessage == "callback":
            msj = message.data
        elif typemessage == "text":
            msj = message.text

        doc_update = {"id": str(id_user), "username": username, "datetime": last_access, "data": msj}
        histrCol.insert_one(doc_update)
        logger.debug("ID: {0} - Username: {1} - Data: {2}".format(id_user, username, msj))

    except Exception as h:
        logger.error("Error al guardar historial en db. {0}".format(h))


# Contactar
def contactar(message, cntct):
    try:
        id_user = message.from_user.id
        name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        last_access = datetime.utcnow()

        user_document = {
            '_id': str(id_user),
            'username': username,
            'name': name,
            'lastName': last_name,
            'lastAccess': last_access,
            'contactar': cntct
        }

        userColl.update_one({"_id": str(id_user)},
                            {"$set": user_document}, upsert=True)

    except Exception as e:
        logger.error(e)


# Cancelar contactar
def cancelarContactar():
    markup = types.InlineKeyboardMarkup()
    bt01 = types.InlineKeyboardButton('Cancelar', callback_data="cancelarcontactar")
    markup.row(bt01)
    return markup


# Devolvemos la fecha del dataset
def fechaDataset(dataset):
    url = "https://analisis.datosabiertos.jcyl.es/api/datasets/1.0/{0}/?extrametas=true&interopmetas=true&source=&timezone=Europe%2FBerlin&lang=es".format(
        dataset)
    res = requestAPI(url)
    date = res['metas']['data_processed']
    date = datetime.fromisoformat(date)
    date_url = datetime.strftime(date, "%Y-%m-%d")
    date_msj = datetime.strftime(date, "%d-%m-%Y")
    return date_url, date_msj

# Devolvemos la fecha del dataset menos 1 dia
def fechaDataset_1(dataset):
    url = "https://analisis.datosabiertos.jcyl.es/api/datasets/1.0/{0}/?extrametas=true&interopmetas=true&source=&timezone=Europe%2FBerlin&lang=es".format(
        dataset)
    res = requestAPI(url)
    date = res['metas']['data_processed']
    date = datetime.fromisoformat(date)
    date_url = datetime.strftime(date - timedelta(days=1), "%Y-%m-%d")
    date_msj = datetime.strftime(date, "%d-%m-%Y")
    return date_url, date_msj

# Activar notificacion
def activarNotificacion(message):
    id_user = message.chat.id
    name = message.chat.first_name

    userColl.update_one({"_id": str(id_user)}, {"$set": {"notification": 1}})
    mensaje = "Hola {0}, a partir de ahora recibiras una notificación cada día una vez hayamos actualizado los datos.\n\n".format(
        name)
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=ky_general())


# Desactivar notificacion
def desactivarNotificacion(message):
    id_user = message.chat.id
    name = message.chat.first_name

    userColl.update_one({"_id": str(id_user)}, {"$set": {"notification": 0}})
    mensaje = "Hola {0}, a partir de ahora ya no recibiras la notificación diaria de la actualización de los datos.\n\n".format(
        name)
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=ky_general())


dic = {"av": "Ávila", "bu": "Burgos", "le": "León", "pa": "Palencia", "sa": "Salamanca", "se": "Segovia", "so": "Soria",
       "va": "Valladolid", "za": "Zamora"}

dic_ge = {"av": "Gerencia de Ávila", "bu": "Gerencia de Burgos", "le": "Gerencia de León", "pa": "Gerencia de Palencia",
          "sa": "Gerencia de Salamanca", "se": "Gerencia de Segovia", "so": "Gerencia de Soria",
          "vae": "Gerencia de Valladolid Este", "vao": "Gerencia de Valladolid Oeste", "za": "Gerencia de Zamora",
          "po": "Gerencia de Ponferrada"}

# DATOS
telegram_token = os.environ['TELEGRAM_TOKEN']
mongoconnection = os.environ['URI_MONGODB']
idadmin = int(os.environ['ID_ADMIN'])

# Instanciamos log
logger = logrm.init_log(loggername="bc19cyl-interactivo")

# Objeto HTTP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
timeout = urllib3.Timeout(connect=2, read=5)
retries = urllib3.Retry(connect=1, read=1, redirect=1)
http = urllib3.PoolManager(timeout=timeout, retries=retries)

# Objeto bot telegram
bot = telebot.TeleBot(telegram_token)

# Connect to DB
db = pymongo.MongoClient(mongoconnection).get_database()
userColl = db['Users']
histrCol = db['Historial']
contactCol = db['Contactar']

bot.send_message(idadmin, "⚠️ Bot @covid19cyl_bot iniciado ⚠️")


# Envia teclado inline al mandar comando /start
@bot.message_handler(commands=['start'])
def command_start(message):
    id_user = message.from_user.id
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    registration_date = datetime.utcnow()

    user_document = {
        '_id': str(id_user),
        'username': username,
        'name': name,
        'lastName': last_name,
        'registrationDate': registration_date,
        'lastAccess': registration_date,
        'contactar': 0,
        'notification': 1,
        'last_notification_ok': registration_date
    }
    checkUser(user_document)
    bot.send_message(message.chat.id,
                     "Bienvenido *{0}*!\n\nEste Bot te va a ayudar a consultar todas las estadisticas sobre el COVID-19 de Castilla y León y sus provincias, los datos se actualizarán todos los días entre las 13:00 y las 15:00.\n\nSi tiene alguna pregunta o ha descubierto un fallo en el bot puede ponerse en contacto escribiendo /contactar\nSi quieres consultar otros comandos disponibles puedes usar /help\n\n¿Que información te gustaría consultar?".format(
                         name), parse_mode="Markdown", reply_markup=ky_general())


# Comando de ayuda
@bot.message_handler(commands=['help'])
def command_help(message):
    comandos = ["/help - Muestra la lista de comandos",
                "/contactar - Permite enviar un mensaje al administrador del bot",
                "/activarnotificacion - Activa la notificación diaria de datos actualizados",
                "/desactivarnotificacion - Desactiva la notificación diaria de datos actualizados"]

    id_user = message.from_user.id
    mensaje = "A continuación puede ver todos los comandos disponibles en este bot:\n\n"

    for comando in comandos:
        mensaje = mensaje + comando + "\n"

    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=ky_general())


# Comando para activar la notificacion de actualizacion de datos
@bot.message_handler(commands=['activarnotificacion'])
def command_activarnotificacion(message):
    activarNotificacion(message)


# Comando para desactivar la notificacion de actualizacion de datos
@bot.message_handler(commands=['desactivarnotificacion'])
def command_desactivarnotificacion(message):
    desactivarNotificacion(message)


# Envia teclado inline al mandar comando /contactar
@bot.message_handler(commands=['contactar'])
def command_contactar(message):
    contactar(message, 1)
    mensaje = "Ha seleccionado ponerse en contacto. Por favor escriba su mensaje."
    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=cancelarContactar())


# Entra aqui si es un callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # print(call)

    dbhistorial(call, "callback")

    if call.message:
        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton casos confirmados covid-19
        if call.data == "g1":
            try:
                # Datos generales
                dataset = "situacion-epidemiologica-coronavirus-en-castilla-y-leon"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?refine.fecha={0}&maxpoints=0" \
                      "&y.confirmados.expr=casos_confirmados&y.confirmados.func=SUM&y.confirmados.cumulative=false&y." \
                      "nuevos.expr=nuevos_positivos&y.nuevos.func=SUM&y.nuevos.cumulative=false&y.altas.expr=altas&y." \
                      "altas.func=SUM&y.altas.cumulative=false&y.fallecimientos.expr=fallecimientos&y.fallecimientos." \
                      "func=SUM&y.fallecimientos.cumulative=false&dataset=situacion-epidemiologica-coronavirus-en-" \
                      "castilla-y-leon&timezone=Europe%2FMadrid&lang=es".format(fecha_url)

                # Colsultamos los datos y procesamos
                res = requestAPI(url)

                totales_cyl = int(res[0]["confirmados"])
                nuevos_cyl = int(res[0]["nuevos"])
                altas_cyl = int(res[0]["altas"])
                # fallecimientos_cyl = int(res[0]["fallecimientos"])

                # Fallecimientos totales y no solo en hospitales
                url_fallecidos_provincia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?dataset=tasa-mortalidad-covid-por-zonas-basicas-de-salud&x=provincia&sort=&maxpoints=&y.serie1-1.expr=fallecidos&y.serie1-1.func=SUM&y.serie1-1.cumulative=false&timezone=Europe%2FBerlin&lang=es"
                res_fallecidos_provincia = requestAPI(url_fallecidos_provincia)
                fallecimientos_cyl = 0

                for provincia in res_fallecidos_provincia:
                    fallecimientos_cyl = int(fallecimientos_cyl) + int(provincia["serie1-1"])

                mensaje = "Personas contagiadas por COVID-19 en *Castilla y León* -> {4}\n\n- Casos Confirmados: `{" \
                          "0}`\n- Nuevos casos: `{1}`\n- Altas: `{2}`\n- Fallecimientos: `{3}`".format(totales_cyl,
                                                                                                       nuevos_cyl,
                                                                                                       altas_cyl,
                                                                                                       fallecimientos_cyl,
                                                                                                       fecha_msj)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("confirmados"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # Callback expresion regular para casos confirmados por ciudad
        elif re.match("confirmados_", call.data):
            try:
                sep = call.data.split("_")

                dataset = "situacion-epidemiologica-coronavirus-en-castilla-y-leon"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=situacion-epidemiologica-coronavirus-en-castilla-y-leon&rows=-1&facet=fecha&facet=provincia&refine.fecha={1}&refine.provincia={0}".format(
                    dic[sep[1]], fecha_url)

                # Fallecimientos totales y no solo en hospitales
                url_fallecidos_provincia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?dataset=tasa-mortalidad-covid-por-zonas-basicas-de-salud&x=provincia&sort=&maxpoints=&y.serie1-1.expr=fallecidos&y.serie1-1.func=SUM&y.serie1-1.cumulative=false&timezone=Europe%2FBerlin&lang=es"
                res_fallecidos_provincia = requestAPI(url_fallecidos_provincia)
                fallecimientos = 0

                for provincia in res_fallecidos_provincia:

                    if provincia["x"] == dic[sep[1]]:
                        fallecimientos = int(provincia["serie1-1"])

                # Colsultamos los datos y procesamos
                res = requestAPI(url)

                totales = int(res["records"][0]["fields"]["casos_confirmados"])
                nuevos = int(res["records"][0]["fields"]["nuevos_positivos"])
                altas = int(res["records"][0]["fields"]["altas"])
                provincia = res["records"][0]["fields"]["provincia"]

                mensaje = "Personas contagiadas por COVID-19 en *{0}* -> {5}\n\n- Casos Confirmados: `{1}`\n- Nuevos " \
                          "casos: `{2}`\n- Altas: `{3}`\n- Fallecimientos: `{4}`".format(
                    provincia, totales, nuevos, altas, fallecimientos, fecha_msj)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g1", "Consultar otra ciudad"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton posibles casos confirmados covid-19
        elif call.data == "g2":
            try:
                mensaje = "A continuación podrá ver los posibles casos de COVID-19 de la gerencia que usted elija."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kygerencias("ger"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # Callback expresion regular para casos por gerencia
        elif re.match("ger", call.data):
            try:
                sep = call.data.split("_")

                # Dataset
                dataset = "tasa-enfermos-acumulados-por-areas-de-salud"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?rows=1000&refine.nombregerencia" \
                      "={0}&dataset=tasa-enfermos-acumulados-por-areas-de-salud&x=fecha.year&x=zbs_geo&sort=x.fecha." \
                      "year,x.zbs_geo&maxpoints=&y.serie1-1.expr=totalenfermedad&y.serie1-1.func=SUM&y.serie1-1." \
                      "cumulative=false&timezone=Europe%2FBerlin&lang=es".format(dic_ge[sep[1]])

                fecha_dat = datetime.strftime(datetime.strptime(fecha_url, "%Y-%m-%d") - timedelta(days=1), "%Y-%m-%d")
                url_dia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=tasa-enfermos-" \
                          "acumulados-por-areas-de-salud&q=&rows=-1&facet=fecha&facet=nombregerencia&facet=zbs_geo&" \
                          "facet=municipio&refine.fecha={0}&refine.nombregerencia={1}".format(fecha_dat, dic_ge[sep[1]])

                dataset2 = "prevalencia-coronavirus"
                fecha_url2, fecha_msj2 = fechaDataset(dataset2)
                fecha_dat2 = datetime.strftime(datetime.strptime(fecha_url2, "%Y-%m-%d") - timedelta(days=1),
                                               "%Y-%m-%d")

                url_prevalencia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=prevalencia" \
                                  "-coronavirus&q=&rows=-1&facet=fecha&facet=zbs_geo&facet=nombregerencia&refine.fecha" \
                                  "={0}&refine.nombregerencia={1}".format(fecha_dat2, dic_ge[sep[1]])

                # Colsultamos los datos y procesamos
                gerencias_ordeenados = {}
                res_gerencia = requestAPI(url)

                infectados_hoy = {}
                res_infectados_hoy = requestAPI(url_dia)

                prevalencia = {}
                res_prevalecencia = requestAPI(url_prevalencia)

                # Guardamos en diccionario y ordenamos
                for g in res_gerencia:
                    gerencias_ordeenados[g["x"]["zbs_geo"]] = g["serie1-1"]

                for infectados in res_infectados_hoy["records"]:
                    infectados_hoy[infectados["fields"]["zbs_geo"]] = infectados["fields"]["totalenfermedad"]

                for infc_prev in res_prevalecencia["records"]:
                    prevalencia[infc_prev["fields"]["zbs_geo"]] = infc_prev["fields"]["prevalencia"]

                # Ordenamos por valor e invertimos
                gerencias_ordeenados = sorted(prevalencia.items(), key=operator.itemgetter(1), reverse=True)
                mensaje = "Posibles casos de COVID-19 en la *{0}* -> {1}\n\n".format(dic_ge[sep[1]], fecha_msj)

                for g in gerencias_ordeenados:
                    mensaje = mensaje + "_{0}:_\nActivos: `{2}` - Nuevos: `{3}`\n\n".format(
                        g[0], int(g[1]), prevalencia[g[0]], infectados_hoy[g[0]])

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g2", "Consultar otra gerencia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton Situación actual en hospitales
        elif call.data == "g3":
            try:
                mensaje = "A continuación podrá ver el estado de los hospitales de la provincia que seleccione."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("hosp"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        elif re.match("hosp", call.data):
            try:
                sep = call.data.split("_")

                # Dataset
                dataset = "situacion-de-hospitalizados-por-coronavirus-en-castilla-y-leon"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=situacion-de" \
                      "-hospitalizados-por-coronavirus-en-castilla-y-leon&rows=-1&facet=fecha&facet=provincia&refine" \
                      ".provincia={0}&refine.fecha={1}".format(dic[sep[1]], fecha_url)

                # Colsultamos los datos y procesamos
                hospitales = {}
                res_hospitales = requestAPI(url)

                for datos in res_hospitales["records"]:
                    hospital = datos["fields"]["hospital"]
                    if hospital not in hospitales:
                        hospitales[hospital] = {"altas": 0, "nuevas_altas": 0, "fallecimientos": 0,
                                                "hospitalizados_planta": 0, "hospitalizados_uci": 0,
                                                "nuevos_fallecimientos": 0, "nuevos_hospitalizados_planta": 0,
                                                "nuevos_hospitalizados_uci": 0}

                    hospitales[hospital]["altas"] = datos["fields"]["altas"]
                    hospitales[hospital]["fallecimientos"] = datos["fields"]["fallecimientos"]
                    hospitales[hospital]["hospitalizados_planta"] = datos["fields"]["hospitalizados_planta"]
                    hospitales[hospital]["hospitalizados_uci"] = datos["fields"]["hospitalizados_uci"]
                    hospitales[hospital]["nuevos_fallecimientos"] = datos["fields"]["nuevos_fallecimientos"]
                    hospitales[hospital]["nuevos_hospitalizados_planta"] = datos["fields"][
                        "nuevos_hospitalizados_planta"]
                    hospitales[hospital]["nuevos_hospitalizados_uci"] = datos["fields"]["nuevos_hospitalizados_uci"]

                mensaje = "Estado de los hospitales de la provincia de *{0}* -> {1}\n\n".format(dic[sep[1]], fecha_msj)

                for key in hospitales.keys():
                    hospitalizados_planta = hospitales[key]["hospitalizados_planta"]
                    nuevos_hospitalizados_planta = hospitales[key]["nuevos_hospitalizados_planta"]
                    hospitalizados_uci = hospitales[key]["hospitalizados_uci"]
                    nuevos_hospitalizados_uci = hospitales[key]["nuevos_hospitalizados_uci"]
                    fallecimientos = hospitales[key]["fallecimientos"]
                    nuevos_fallecimientos = hospitales[key]["nuevos_fallecimientos"]
                    altas = hospitales[key]["altas"]
                    nuevas_altas = hospitales[key]["nuevas_altas"]

                    mensaje = mensaje + "_{0}_\nAltas: `{1}`\nNuevas altas: `{2}`\nHospitalizados en planta: `{3}`\nNuevos hospitalizados en planta: `{4}`\nHospitalizados en UCI: `{5}`\nNuevos hospitalizados en UCI: `{6}`\nFallecimientos: `{7}`\nNuevos fallecimientos: `{8}`\n\n".format(
                        key, altas, nuevas_altas, hospitalizados_planta, nuevos_hospitalizados_planta,
                        hospitalizados_uci, nuevos_hospitalizados_uci, fallecimientos, nuevos_fallecimientos)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g3", "Consultar otra provincia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())
        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton ocupacion actual en hospitales
        elif call.data == "g4":
            try:
                mensaje = "A continuación podrá ver el estado de ocupación de los hospitales de la provincia que seleccione."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("ocuphosp"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        elif re.match("ocuphosp", call.data):
            try:
                sep = call.data.split("_")

                # Dataset
                dataset = "ocupacion-de-camas-en-hospitales"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=ocupacion-de-camas-en" \
                      "-hospitales&facet=fecha&facet=provincia&refine.provincia={0}&refine.fecha={1}".format(
                    dic[sep[1]], fecha_url)

                # Colsultamos los datos y procesamos
                ocup_hospitales = {}
                res_ocuphospitales = requestAPI(url)

                for datos in res_ocuphospitales["records"]:
                    hospital = datos["fields"]["hospital"]
                    if hospital not in ocup_hospitales:
                        ocup_hospitales[hospital] = {"camas_habilitadas_planta": 0, "camas_habilitadas_uci": 0,
                                                     "camas_iniciales_planta": 0,
                                                     "camas_iniciales_uci": 0, "camas_ocupadas_planta": 0,
                                                     "camas_ocupadas_uci": 0}

                    ocup_hospitales[hospital]["camas_habilitadas_planta"] = datos["fields"]["camas_habilitadas_planta"]
                    ocup_hospitales[hospital]["camas_habilitadas_uci"] = datos["fields"]["camas_habilitadas_uci"]
                    ocup_hospitales[hospital]["camas_iniciales_planta"] = datos["fields"]["camas_iniciales_planta"]
                    ocup_hospitales[hospital]["camas_iniciales_uci"] = datos["fields"]["camas_iniciales_uci"]
                    ocup_hospitales[hospital]["camas_ocupadas_planta"] = datos["fields"]["camas_ocupadas_planta"]
                    ocup_hospitales[hospital]["camas_ocupadas_uci"] = datos["fields"]["camas_ocupadas_uci"]

                mensaje = "Ocupación de los hospitales de la provincia de *{0}* -> {1}\n\n".format(dic[sep[1]],
                                                                                                   fecha_msj)

                for key in ocup_hospitales.keys():
                    camas_habilitadas_planta = ocup_hospitales[key]["camas_habilitadas_planta"]
                    camas_habilitadas_uci = ocup_hospitales[key]["camas_habilitadas_uci"]
                    camas_iniciales_planta = ocup_hospitales[key]["camas_iniciales_planta"]
                    camas_iniciales_uci = ocup_hospitales[key]["camas_iniciales_uci"]
                    camas_ocupadas_planta = ocup_hospitales[key]["camas_ocupadas_planta"]
                    camas_ocupadas_uci = ocup_hospitales[key]["camas_ocupadas_uci"]

                    mensaje = mensaje + "_{0}_\n- Camas iniciales planta: `{1}`\n- Camas habilitadas planta: " \
                                        "`{2}`\n- Camas ocupadas en planta: `{3}`\n- Camas iniciales UCI: `{4}`\n- " \
                                        "Camas habilitadas en UCI: `{5}`\n- Camas ocupadas en UCI: `{6}`\n\n".format(
                        key, camas_iniciales_planta, camas_habilitadas_planta, camas_ocupadas_planta,
                        camas_iniciales_uci, camas_habilitadas_uci, camas_ocupadas_uci)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g3", "Consultar otra provincia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())
        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton Situación actual en hospitales
        elif call.data == "g5":
            try:
                mensaje = "A continuación podrá ver la cantidad de test realizados para detectar el COVID-19 en la provincia que seleccione."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("test"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        elif re.match("test", call.data):
            try:
                sep = call.data.split("_")

                # Dataset
                dataset = "pruebas-realizados-coronavirus"
                fecha_url, fecha_msj = fechaDataset(dataset)
                fecha_url = datetime.strftime(datetime.strptime(fecha_url, "%Y-%m-%d") - timedelta(days=1), "%Y-%m-%d")

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=pruebas-realizados-coronavirus&facet=fecha&facet=provincia&refine.provincia={0}&refine.fecha={1}".format(
                    dic[sep[1]], fecha_url)

                # Colsultamos los datos y procesamos
                res_test = requestAPI(url)

                pcr_positivos = res_test["records"][0]["fields"]["pcr_positivos"]
                pcr_total = res_test["records"][0]["fields"]["pcr_total"]
                test_rapidos_positivos = res_test["records"][0]["fields"]["test_rapidos_positivos"]
                test_rapidos_total = res_test["records"][0]["fields"]["test_rapidos_total"]
                total_pruebas = res_test["records"][0]["fields"]["total_pruebas"]
                total_pruebas_positivas = res_test["records"][0]["fields"]["total_pruebas_positivas"]

                mensaje = "Total de test realizados en la provincia de *{0}* -> {7}\n\nTotal pruebas: `{1}`\nTotal pruebas positivas: `{2}`\nTotal PCR: `{3}`\nTotal PCR positivos: `{4}`\nTotal test rapidos: `{5}`\nTotal test rapidos positivos: `{6}`".format(
                    dic[sep[1]], total_pruebas, total_pruebas_positivas, pcr_total, pcr_positivos, test_rapidos_total,
                    test_rapidos_positivos, fecha_msj)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g5", "Consultar otra provincia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())
        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton mortalidad
        elif call.data == "g6":
            try:
                mensaje = "A continuación podrá ver las estadisticas de mortalidad de la gerencia que usted elija."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kygerencias("morger"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # Callback expresion regular para casos por gerencia
        elif re.match("morger", call.data):
            try:
                sep = call.data.split("_")

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?refine.nombregerencia={0}" \
                      "&dataset=tasa-mortalidad-covid-por-zonas-basicas-de-salud&x=nombregerencia&x=zbs_geo&sort=" \
                      "x.nombregerencia,x.zbs_geo&maxpoints=&y.serie1-1.expr=fallecidos&y.serie1-1.func=SUM&y.serie1-1" \
                      ".cumulative=false&timezone=Europe%2FBerlin&lang=es".format(dic_ge[sep[1]])

                # Colsultamos los datos y procesamos
                gerencias_ordeenados = {}
                res_gerencia = requestAPI(url)

                # Guardamos en diccionario y ordenamos
                for g in res_gerencia:
                    gerencias_ordeenados[g["x"]["zbs_geo"]] = g["serie1-1"]

                # Ordenamos por valor e invertimos
                gerencias_ordeenados = sorted(gerencias_ordeenados.items(), key=operator.itemgetter(1), reverse=True)

                mensaje = "Mortalidad por COVID-19 en la *{0}*\n\n".format(dic_ge[sep[1]])

                for g in gerencias_ordeenados:
                    mensaje = mensaje + "{0}: `{1}`\n".format(g[0], int(g[1]))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g6", "Consultar otra gerencia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton Fase de desescalada
        elif call.data == "g8":
            try:
                mensaje = "A continuación podrá ver en la fase de desescalada en la que se encuentran las Zonas de Salud de su provincia."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kygerencias("desescalada"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Callback expresion regular para desescalada
        elif re.match("desescalada", call.data):
            try:
                sep = call.data.split("_")

                dataset = "fases-desescalada"
                fecha_url, fecha_msj = fechaDataset(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=fases-desescalada&q=&rows=-1&sort=-fecha&facet=fecha&facet=nombregerencia&facet=fase_desescalada&facet=zbs_geo&facet=municipio&refine.nombregerencia={0}".format(
                    dic_ge[sep[1]])

                desescalada = {}

                # Colsultamos los datos y procesamos
                res_desescalada = requestAPI(url)

                mensaje = "Fases de desescalada en la *{0}* -> {1}\n\n".format(dic_ge[sep[1]], fecha_msj)

                for g in res_desescalada["records"]:
                    desescalada[g["fields"]["zbs_geo"]] = g["fields"]["fase_desescalada"]

                for poblacion, fase in desescalada.items():
                    mensaje = mensaje + "_{0}:_\n`{1}`\n\n".format(poblacion, fase)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g8", "Consultar otra gerencia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa el boton de Indicadores de Riesgo
        elif call.data == "g9":
            try:
                mensaje = "A continuación podrá ver el porcentaje de Indicadores de Riesgo en su provincia."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("indicadorriesgo"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # Callback expresion regular para indicadores de riesgo
        elif re.match("indicadorriesgo", call.data):
            try:
                sep = call.data.split("_")
                dataset = "indicadores-de-riesgo-covid-19-por-provincias"
                fecha_url, fecha_msj = fechaDataset_1(dataset)

                url = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=indicadores-de-" \
                      "riesgo-covid-19-por-provincias&q=&facet=fecha&facet=provincia&facet=indicador&facet=valoracion" \
                      "&refine.fecha={0}&refine.provincia={1}".format(fecha_url, dic[sep[1]])

                # Colsultamos los datos y procesamos
                res_indicadores = requestAPI(url)

                mensaje = u"\U0001F9A0 Indicadores de Riesgo en *{0}* -> {1}\n\n".format(dic[sep[1]], fecha_msj)

                leyenda = {"Riesgo controlado": "🟢", "Nueva normalidad": "🟢", "Bajo": "🟡", "Medio": "🟠", "Alto": "🔴", "Muy alto": "⚫"}

                for data in res_indicadores["records"]:
                    fecha = data["fields"]["fecha"]
                    indicador = data["fields"]["indicador"]
                    if "valor" in data["fields"]:
                        valor = data["fields"]["valor"]
                    else:
                        valor = "-"
                    valoracion = data["fields"]["valoracion"]

                    mensaje = "{0}*{1}*\n".format(mensaje, indicador)
                    mensaje = "{0}- Valor: *{1}*\n".format(mensaje, valor)
                    mensaje = "{0}- Valoración: *{1}* {2}\n\n".format(mensaje, valoracion, leyenda[valoracion])

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g9", "Consultar otra provincia"))

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa el boton de Vacunaciones
        elif call.data == "g10":
            try:
                url_recibidas = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?disjunctive.provincia=true&sort=fecha&refine.fecha=2021-01-25&y.serie1.expr=total_vacunas_recibidas&y.serie1.func=SUM&dataset=vacunas-recibidas-covid&timezone=Europe%2FMadrid&lang=es"
                url_vacunadas = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?disjunctive.provincia=true&y.serie1.expr=dosis_administradas&y.serie1.func=SUM&dataset=personas-vacunadas-covid&timezone=Europe%2FMadrid&lang=es"
                url_vacunadas_cicloclompletoo = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?disjunctive.provincia=true&y.serie1.expr=personas_vacunadas_ciclo_completo&y.serie1.func=SUM&dataset=personas-vacunadas-covid&timezone=Europe%2FMadrid&lang=es"

                total_recibidas = requestAPI(url_recibidas)
                total_vacunadas = requestAPI(url_vacunadas)
                total_vacunadas_ciclocompleto = requestAPI(url_vacunadas_cicloclompletoo)

                total_recibidas = int(total_recibidas[0]["serie1"])
                total_vacunadas = int(total_vacunadas[0]["serie1"])
                total_vacunadas_ciclocompleto = int(total_vacunadas_ciclocompleto[0]["serie1"])

                mensaje = "A continuación podrá ver la cantidad de vacunas y personas vacunadas por cada provincia.\n\n" \
                          "- Vacunas recibidas: *{0}*\n- Dosis administradas: *{1}*\n- Pers. vacunadas ciclo completo: *{2}*".format(
                    total_recibidas, total_vacunadas, total_vacunadas_ciclocompleto)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')

                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyciudades("vacunas"))

            except Exception as g:
                logger.error(g)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())



        # Callback expresion regular para vacunaciones
        elif re.match("vacunas", call.data):
            try:
                sep = call.data.split("_")

                url_totalrecividas_provincia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?disjunctive.provincia=true&refine.provincia={0}&timezone=Europe%2FMadrid&dataset=vacunas-recibidas-covid&x=marca&sort=&maxpoints=&y.serie1-1.expr=total_vacunas_recibidas&y.serie1-1.func=MAX&y.serie1-1.cumulative=false&lang=es".format(dic[sep[1]])
                url_totalvacunadas_provincia = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/analyze/?disjunctive.provincia=true&refine.provincia={0}&timezone=Europe%2FMadrid&dataset=personas-vacunadas-covid&x=provincia&sort=&maxpoints=&y.serie1-1.expr=personas_vacunadas_ciclo_completo&y.serie1-1.func=SUM&y.serie1-1.cumulative=false&y.serie1-2.expr=dosis_administradas&y.serie1-2.func=SUM&y.serie1-2.cumulative=false&lang=es".format(
                    dic[sep[1]])
                url_ultimasvacunadas = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=personas-vacunadas-covid&q=&rows=1&sort=fecha&facet=fecha&facet=provincia&facet=personas_vacunadas&refine.provincia={0}".format(
                    dic[sep[1]])

                totalrecividas_provincia = requestAPI(url_totalrecividas_provincia)
                totalvacunadas_provincia = requestAPI(url_totalvacunadas_provincia)
                ultimasvacunadas = requestAPI(url_ultimasvacunadas)

                msg_totalrecividas_provincia = ""
                for marca in totalrecividas_provincia:
                    msg_totalrecividas_provincia = msg_totalrecividas_provincia + "    - {0}: *{1}*\n".format(
                        marca["x"], int(marca["serie1-1"]))

                total_dosisadministradas = int(totalvacunadas_provincia[0]["serie1-2"])
                total_dosisadministradas_ciclocompleto = int(totalvacunadas_provincia[0]["serie1-1"])
                msg_totaldosis_provincia = "    - Dosis administradas: *{0}*\n    - Pers. vacunas ciclo completo: *{1}*".format(
                    total_dosisadministradas, total_dosisadministradas_ciclocompleto)

                uv_fecha = ultimasvacunadas["records"][0]["fields"]["fecha"]
                uv_fecha = datetime.strptime(uv_fecha, "%Y-%m-%d")
                uv_fecha = datetime.strftime(uv_fecha, "%d-%m-%Y")
                dosis_ultimodia = ultimasvacunadas["records"][0]["fields"]["dosis_administradas"]
                ciclocompleto_ultimodia = ultimasvacunadas["records"][0]["fields"]["personas_vacunadas_ciclo_completo"]

                mensaje = "Vacunaciones en la provincia de *{0}*\n\nTotal recibidas:\n{1}\nTotal vacunadas:\n{2}" \
                          "\n\nÚltimo día -> {3}\n    - Dosis administradas: *{4}*\n    - Pers. vacunadas ciclo completo: *{5}*".format(
                    dic[sep[1]], msg_totalrecividas_provincia, msg_totaldosis_provincia, uv_fecha, dosis_ultimodia,
                    ciclocompleto_ultimodia)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyvolver("g10", "Consultar otra provincia"))

            except Exception as g:
                logger.error(g)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        # Si pulsa boton Ajustes
        elif call.data == "g7":
            try:
                mensaje = "A continuación podrá Activar/Desactivar la notificación diaria de actualización de datos.\n\nEsta notificación por defecto se envia todos los días informandole de que hemos actualizado los datos. De esta manera no tendrá que preocuparse de tener que comprobarlo cada poco tiempo."

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=mensaje,
                                      parse_mode='Markdown')
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=kyajustes())

            except Exception as f:
                logger.error(f)
                bot.send_message(call.message.chat.id,
                                 "Lo sentimos, se ha producido un error al consultar los datos. Intentelo de nuevo "
                                 "mas tarde.", reply_markup=ky_general())


        # Callback botones activar/descativar notificaciones
        elif call.data == "activarnotificacion":
            activarNotificacion(call.message)

        elif call.data == "desactivarnotificacion":
            desactivarNotificacion(call.message)

        # ---------------------------------------------------------------------------------------------------------------
        # Callback para enviar el teclado del menu principal
        elif call.data == "menuprincipal":
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup="")
            bot.send_message(call.message.chat.id, "¿Que información te gustaría consultar?", reply_markup=ky_general())

        # ---------------------------------------------------------------------------------------------------------------
        elif call.data == "cancelarcontactar":
            contactar(call, 0)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup="")
            bot.send_message(call.message.chat.id, "¿Que información te gustaría consultar?", reply_markup=ky_general())


# Procesamos otros mensajes
@bot.message_handler(func=lambda message: True)
def message_other(message):
    # print(message)
    dbhistorial(message, "text")

    # Comprobamos si contactar = 1
    documento = userColl.find_one({"_id": str(message.from_user.id), "contactar": 1})

    if documento:
        mensaje = "Muchas gracias por ponerte en contacto. Leeremos tu mensaje tan pronto nos sea posible."
        contactar(message, 0)
        bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=ky_general())

        id_user = message.from_user.id
        name = message.from_user.first_name
        text = message.text

        mensaje_admin = "------ Nuevo mensaje ------\nID: {0}\nNombre: {1}\nMensaje: {2}".format(id_user, name, text)
        bot.send_message(idadmin, mensaje_admin, parse_mode="Markdown")
        logger.debug("Enviamos mensaje: {0}".format(mensaje_admin))

    else:
        bot.send_message(message.chat.id, "¿Que información te gustaría consultar?", reply_markup=ky_general())


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
