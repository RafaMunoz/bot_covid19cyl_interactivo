#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime, timedelta
import pymongo
import telebot
import urllib3
from telebot import types
from telebot.apihelper import ApiTelegramException
import logrm
import time

# Request to API data
def request_api(argurl):
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


# Devolvemos la fecha del dataset
def fecha_dataset(dataset):
    url = "https://analisis.datosabiertos.jcyl.es/api/datasets/1.0/{0}/?extrametas=true&interopmetas=true&source=" \
          "&timezone=Europe%2FBerlin&lang=es".format(dataset)
    res = request_api(url)
    date = res['metas']['data_processed']
    date = datetime.fromisoformat(date)
    return date


# Envia keyboard principal
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
    #bt07 = types.InlineKeyboardButton('Fase de Desescalada', callback_data="g8")
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


# DATOS
telegram_token = os.environ['TELEGRAM_TOKEN']
mongoconnection = os.environ['URI_MONGODB']


# Instanciamos log
logger = logrm.init_log(loggername="bc19cyl-checkdataset")


# Objeto HTTP
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

# Objeto bot telegram
bot = telebot.TeleBot(telegram_token)

# Connect to DB
db = pymongo.MongoClient(mongoconnection).get_database()
userColl = db['Users']
settingsCol = db['Settings']

doc_settings = settingsCol.find_one({"_id": "datasets"})
doc_dataset = []
notificar = 0

for dataset in doc_settings["datasets"]:
    date_dataset = fecha_dataset(dataset["name"])

    date_db = dataset["last_update"]
    date_dataset = datetime.strftime(date_dataset, "%Y-%m-%d %H:%M:%S")

    if date_db != date_dataset:
        logger.debug("Actualizado {0} - {1}".format(dataset["name"], date_dataset))
        doc_dataset.append({"name": dataset["name"], "last_update": date_dataset})
        notificar = notificar + 1

    else:
        logger.debug("No actualizado {0} - {1}".format(dataset["name"], date_dataset))

if notificar == len(doc_settings["datasets"]):

    time.sleep(120)
    usuarios = userColl.find({"notification": 1})

    for usuario in usuarios:
        id_usuario = int(usuario["_id"])
        name = usuario["name"]

        mensaje = "📢 Hola {0}, le informamos de que ya hemos actualizado los datos de hoy -> {1}\n\n¿Que información te gustaría consultar?".format(
            name, datetime.strftime(datetime.now(), "%d-%m-%Y"))

        try:
            bot.send_message(id_usuario, mensaje, parse_mode="Markdown", reply_markup=ky_general())
            logger.debug("Notificamos {0} {1}".format(id_usuario, name))
            userColl.update_one({"_id": str(id_usuario)}, {"$set": {"last_notification_ok": datetime.utcnow()}})

        except ApiTelegramException as te:
            error_code = int(te.error_code)

            if error_code == 403:
                logger.error("Bot bloqueado por el usuario {0}. Desactivamos notificaciones.".format(id_usuario))
                userColl.update_one({"_id": str(id_usuario)}, {"$set": {"notification": 0}})

        except Exception as e:
            logger.error("ERROR {0} {1}. {2}".format(id_usuario, name, e))


        # Si durante 15 dias se ha producido error al notificar le deshabilitamos las notificaciones
        inactive = (datetime.now() - usuario["last_notification_ok"]) / timedelta(days=1)

        if inactive > 15:
            logger.info("Inactivo durante {0} days. Deshabilitamos {1}".format(round(inactive, 2), id_usuario))
            userColl.update_one({"_id": str(id_usuario)}, {"$set": {"notification": 0}})

    settingsCol.update_one({"_id": "datasets"}, {"$set": {"datasets": doc_dataset}})
