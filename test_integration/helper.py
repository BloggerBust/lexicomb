from bbpyp.lexicomb_engine.bootstrap import Bootstrap as LEngineBootstrap
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum


class Helper():
    def __init__(self):
        self._lexicomb_ioc = None
        self._lexicomb_parser = None
        self._lexer = None
        self.bootstrap()

    def bootstrap(self):
        app_config = {
            "logger": {
                "version": 1,
                "formatters": {
                    "detailed": {
                        "class": "logging.Formatter",
                        "format": "%(asctime)s [%(relativeCreated)6d] [%(name)s - %(levelname)s] [%(module)s::%(funcName)s] = %(message)s"
                    },
                    "standard": {
                        "class": "logging.Formatter",
                        "format": "[%(name)s - %(levelname)s] [%(module)s::%(funcName)s] = %(message)s"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "DEBUG",
                        "formatter": "standard"
                    },
                    "root_file": {
                        "class": "logging.FileHandler",
                        "filename": "trip_log.log",
                        "mode": "w",
                        "formatter": "detailed"
                    },
                    "message_bus_file": {
                        "class": "logging.FileHandler",
                        "filename": "message_bus.log",
                        "mode": "w",
                        "formatter": "detailed"
                    },
                    "lexical_state_machine_file": {
                        "class": "logging.FileHandler",
                        "filename": "lexical_state_machine.log",
                        "mode": "w",
                        "formatter": "detailed"
                    },
                    "lexicomb_file": {
                        "class": "logging.FileHandler",
                        "filename": "lexicomb_file.log",
                        "mode": "w",
                        "formatter": "detailed"
                    },
                },
                "loggers": {
                    "development": {
                        "level": "ERROR",
                        "handlers": ["console"]
                    },
                    "production": {
                        "level": "ERROR",
                        "handlers": ["root_file"]
                    },
                    "message_bus": {
                        "level": "ERROR",
                        "handlers": ["console", "message_bus_file"],
                    },
                    "lexical_state_machine": {
                        "level": "ERROR",
                        "handlers": ["console", "lexical_state_machine_file"],
                    },
                    "lexicomb": {
                        "level": "ERROR",
                        "handlers": ["console", "lexicomb_file"],
                    },
                },
                "root": {
                    'level': 'ERROR',
                    'handlers': ['root_file']
                }
            },
            "default_logger": "production",
            "memory_channel_max_buffer_size": 0,
            "lexicomb": {
                "src": "test_integration/lexicomb/src/"
            }
        }

        lexicomb_engine = LEngineBootstrap(app_config, lambda *args, **kwargs: None)

        self._lexicomb_ioc = lexicomb_engine.lexicomb_ioc
        self._lexicomb_parser = lexicomb_engine.lexicomb_ioc.parser_provider()
        self._lexer = lexicomb_engine.lexicomb_ioc.lexer_provider()
        self._result_factory = self._lexicomb_ioc.result_factory_provider

    def tokenize(self, input_line):
        return self._lexer.tokenize(input_line)

    @property
    def lexicomb_parser(self):
        return self._lexicomb_parser

    @property
    def lexicomb_ioc(self):
        return self._lexicomb_ioc

    def create_operator_enum(self, operator):
        return OperatorEnum(operator)
