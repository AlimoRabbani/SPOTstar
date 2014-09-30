__author__ = 'Alimohammad'

import json
import logging


class Config:
    config = dict()
    db_config = dict()
    logger = logging.getLogger("SPOTlight Decision")
    service_logger = logging.getLogger("SPOTlight Decision Services")

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        Config.config = json.loads(open("decision_config.json").read())
        Config.db_config = json.loads(open("db.json").read())
        Config.config["mac_address"] = Config.get_mac('wlan0')

        logger = logging.getLogger("SPOTlight Decision")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('decision.log')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        service_logger = logging.getLogger("SPOTlight Decision Services")
        service_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('decision_services.log')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        service_logger.addHandler(file_handler)
        service_logger.addHandler(console_handler)

        Config.logger.info("Configurations loaded...")

    @staticmethod
    def get_mac(interface):
        # Return the MAC address of interface
        try:
            mac_address = open("/sys/class/net/%s/address" % interface).readline()
        except:
            mac_address = "00:00:00:00:00:00"
        return mac_address[0:17]