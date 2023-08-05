"""
CARPI DAEMON COMMONS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from configparser import ConfigParser
from os import environ
from sys import stderr

from carpicommons.errors import ExitCodes, CarPiExitException, ConfigFileLoadError
from carpicommons.log import log_unhandled_exception, configure_logging


class Daemon(object):
    def __init__(self,
                 daemon_name: str):
        self._daemon_name = daemon_name
        self._config: ConfigParser = None

    def set_config(self, config: ConfigParser):
        """
        Sets a pre-loaded configuration
        """
        self._config = config
        self._configure_logging()

    def _get_config(self, section: str, key: str, fallback: str=object()) -> str:
        """
        Gets a string config value
        :param section: Section
        :param key: Key
        :param fallback: Optional fallback value
        """
        return self._config.get(section, key, fallback=fallback)

    def _get_config_float(self, section: str, key: str, fallback: float=object()) -> float:
        """
        Gets a float config value
        :param section: Section
        :param key: Key
        :param fallback: Optional fallback value
        """
        return self._config.getfloat(section, key, fallback=fallback)

    def _get_config_int(self, section: str, key: str, fallback: int=object()) -> int:
        """
        Gets an int config value
        :param section: Section
        :param key: Key
        :param fallback: Optional fallback value
        """
        return self._config.getint(section, key, fallback=fallback)

    def _get_config_bool(self, section: str, key: str, fallback: bool=object()) -> bool:
        """
        Gets a boolean config value
        :param section: Section
        :param key: Key
        :param fallback: Optional fallback value
        """
        return self._config.getboolean(section, key, fallback=fallback)

    def _configure_logging(self):
        """
        Configures logging (used as a callback after initializing config)
        """
        configure_logging([
            self._get_config('Logging', 'path', '')
        ])

    @property
    def name(self):
        return self._daemon_name

    def startup(self):
        raise NotImplementedError

    def shutdown(self):
        pass


class DaemonRunner(object):
    def __init__(self,
                 env_config_var: str,
                 default_config_paths: list=[]):
        self._config_paths = self._build_config_file_list(env_config_var,
                                                          default_config_paths)

    def _build_config_file_list(self,
                                env_config_var: str,
                                default_config_paths: list) -> list:
        files = []
        if env_config_var in environ:
            files.append(environ.get(env_config_var))
        files += default_config_paths
        return files

    def _read_config(self) -> ConfigParser:
        config = ConfigParser()
        for file in self._config_paths:
            try:
                print("Trying to load configuration {} ...".format(file),
                      file=stderr)
                config.read_file(open(file))
                return config
            except IOError:
                pass

        print("Failed to load any of these configuration files!\n"
              "{}".format("\n".format(self._config_paths)),
              file=stderr)
        raise ConfigFileLoadError(';'.join(self._config_paths))

    def run(self, daemon: Daemon):
        exit_code = 0

        try:
            daemon.set_config(self._read_config())
            daemon.startup()
        except (KeyboardInterrupt, SystemExit):
            exit_code = ExitCodes.OK
        except CarPiExitException as e:
            exit_code = e.exit_code
        except:
            exit_code = ExitCodes.UNKNOWN
            log_unhandled_exception()
        finally:
            daemon.shutdown()

        exit(exit_code)
