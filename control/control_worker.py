#!/usr/bin/env python

__author__ = 'Alimohammad'

import rpyc
from rpyc.utils.server import ThreadedServer
import threading

from reactive_control import ReactiveControl
from config import Config
from control_updater import Updater


class DecisionService(rpyc.Service):
    @staticmethod
    def exposed_temperature_updated(temperature):
        temperature_thread = threading.Thread(target=ReactiveControl.temperature_updated, args=(temperature, ))
        temperature_thread.daemon = True
        temperature_thread.start()

    @staticmethod
    def exposed_motion_updated(standard_deviation):
        motion_thread = threading.Thread(target=ReactiveControl.motion_updated, args=(standard_deviation, ))
        motion_thread.daemon = True
        motion_thread.start()

if __name__ == "__main__":
    Config.initialize()
    Config.logger.info("SPOTlight control worker started...")
    Updater.start()
    server = ThreadedServer(DecisionService, hostname=Config.service_config["control_service_address"],
                            port=Config.service_config["control_service_port"], logger=Config.service_logger,
                            authenticator=None)
    server.start()
    Config.logger.info("SPOTlight control worker shutting down...")
