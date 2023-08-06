import statsd

from . import Base
from .config import Configuration
from .config.parser import ApacheConfigParser, ConfigParserBase
from .config.store import FileStore, RedisStore

CONFIG_STORE_MAP = {"file": FileStore, "redis": RedisStore}


def _parse_global_config(filename, config_parser: ConfigParserBase):
    """Parse config file with given config_parser.

    :param filename: filename
    :type filename: str
    :param config_parser: config parser to use
    :type config_parser: ConfigParserBase
    :return: config
    :rtype: dict
    """
    with open(filename, "r", encoding="utf-8") as config_file:
        content = config_file.read()

    return config_parser.parse(content)


class InfrastructureFactory(Base):
    """Infrastructure factory class.

    The infrastructure factory will create instances of registered
    "infrastructure" classes, with configuration for a specific hostname.
    """

    slots = [
        "global_config",
        "instance_config",
        "registered_infrastructure",
        "config_parser",
    ]

    def __init__(
        self, config_file: str, config_parser: ConfigParserBase = None
    ):
        """Initialize an application service factory.

        After reading the configuration, it also configures the defaults
        in the statsd module.

        :param config_file: Global configuration file to read
        :type config_file: str
        :param config_parser: config parser used to parse global configuration
        :type config_parser: ConfigParserBase
        :param hostname: Hostname to retrieve host-specific configuration for
        :type hostname: str
        """
        if config_parser is None:
            config_parser = ApacheConfigParser

        self.config_parser = config_parser()

        self.logger.info(f"Using configuration file '{config_file}'")
        self.global_config = _parse_global_config(
            filename=config_file, config_parser=self.config_parser
        )

        config_store_type = self.global_config["InstanceConfig"]["type"]

        if config_store_type == "none":
            self.instance_config = None
        else:
            config_store_args = self.global_config["InstanceConfig"][
                "arguments"
            ]

            config_store = CONFIG_STORE_MAP[config_store_type](
                **config_store_args
            )

            self.instance_config = Configuration(
                parser=ApacheConfigParser(), store=config_store
            )

        if "statsd" in self.global_config:
            if "disabled" in self.global_config["statsd"]:
                self.global_config["statsd"]["disabled"] = bool(
                    int(self.global_config["statsd"]["disabled"])
                )
            statsd.Connection.set_defaults(**self.global_config["statsd"])
        else:
            # No statsd configuration available; forcefully disable it
            statsd.Connection.set_defaults(disabled=True)

        self.registered_infrastructure = {}

    def register_infrastructure(self, cls: type):
        """Register an infrastructure class with the factory.

        :param cls: Class to register in the infrastructure factory
        :type cls: class
        """
        self.registered_infrastructure[cls.__name__] = cls

    def get_infrastructure(self, hostname: str, infrastructure_name: str):
        """Retrieve an infrastructure instance for the selected instance.

        :param infrastructure_name: Name of the infrastructure class to
                                    instantiate
        :type infrastructure_name: str
        :return: [description]
        :rtype: object
        """
        if self.instance_config is None:
            config = {**self.global_config}
        else:
            config = {
                **self.global_config,
                **self.instance_config.get(hostname),
            }

        with self.statsd.get_timer("get_infrastructure").time(
            infrastructure_name
        ):
            infra = self.registered_infrastructure[infrastructure_name](
                config=config
            )

        return infra

    def set_current_event(self, event):
        # cache current event and associate session with it,
        self.logger.info("current_event set")
        pass

    def flush_current_event(self):
        # flush cached session
        self.logger.info("current_event flushed")
        pass
