from pelops.abstractmicroservice import AbstractMicroservice
import skeiron
import skeiron.relayfactory
import skeiron.schema.schema


class Relayservice(AbstractMicroservice):
    _version = skeiron.version

    _relay_list = None

    def __init__(self, config, mqtt_client=None, logger=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        """
        AbstractMicroservice.__init__(self, config, "relayservice", mqtt_client, logger)
        self._relay_list = skeiron.relayfactory.RelayFactory.create_relay_list(self._config,
                                                                               self._mqtt_client, self._logger)
        self._logger.info("Relayservice.__init__ - finished initializing")

    def _start(self):
        self._logger.info("Relayservice._start - starting relays")
        for relay in self._relay_list:
            self._logger.debug("Relayservice._start - starting '{}.{}'".format(type(relay), relay.name))
            relay.start()
        self._logger.info("Relayservice._start - started")

    def _stop(self):
        self._logger.info("Relayservice._stop - stopping relays")
        for relay in self._relay_list:
            self._logger.debug("Relayservice._stop - stopping '{}.{}'".format(type(relay), relay.name))
            relay.stop()
        self._logger.info("Relayservice._stop - stopped")

    @classmethod
    def _get_description(cls):
        return "Skeiron provides a Forwarding/Echo/Collect/Distribute service."

    @classmethod
    def _get_schema(cls):
        return skeiron.schema.schema.get_schema()


def standalone():
    Relayservice.standalone()


if __name__ == "__main__":
    Relayservice.standalone()
