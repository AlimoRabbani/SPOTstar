__author__ = 'Alimohammad'

import json
import logging


class Config:
    db_config = dict()
    service_config = dict()
    logger = logging.getLogger("SPOTlight DB")

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        Config.service_config = json.loads(open("config_service.json").read())
        Config.db_config = json.loads(open("config_db.json").read())

        logger = logging.getLogger("SPOTlight DB")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('db.log')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        Config.logger.info("Configurations loaded...")