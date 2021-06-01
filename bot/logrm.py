#!/usr/bin/python3
# -*- coding: utf-8 -*-
try:
    import graypy
except IOError:
    pass

import logging
import os


# Instanciamos el log
def init_log(loggername=""):
    logger = logging.getLogger(loggername)
    try:
        loglevel = os.environ["LOGLEVEL"]
    except KeyError:
        loglevel = "INFO"

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(loglevel)

    # Log terminal
    handler_terminal = logging.StreamHandler()
    handler_terminal.setFormatter(formatter)
    logger.addHandler(handler_terminal)

    # Graylog
    try:
        logserver_host = os.environ["GRAYLOG_HOST"]
        logserver_port = os.environ["GRAYLOG_PORT"]
        handler_graylog = graypy.GELFUDPHandler(logserver_host, int(logserver_port))
        logger.addHandler(handler_graylog)

    except KeyError:
        pass

    logger.info("STARTED: {0}".format(loggername))
    return logger
