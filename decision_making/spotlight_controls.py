__author__ = 'Alimohammad'

import rpyc
from rpyc.utils.server import ThreadedServer

from reactive_control import ReactiveControl
from decision_config import Config


class DecisionService(rpyc.Service):
    @staticmethod
    def exposed_temperature_updated(temperature):
        ReactiveControl.temperature_updated(temperature)

    @staticmethod
    def exposed_motion_updated(standard_deviation):
        Config.logger.debug("motion update handler called")
        ReactiveControl.motion_updated(standard_deviation)

if __name__ == "__main__":
    Config.initialize()
    Config.logger.info("SPOTlight device manager started...")
    server = ThreadedServer(DecisionService, hostname=Config.config["decision_service_address"],
                            port=Config.config["decision_service_port"], logger=Config.service_logger,
                            authenticator=None)
    server.start()
    Config.logger.info("SPOTlight decision maker shutting down...")
