import logging
from bbpyp.lexicomb_engine.bootstrap import Bootstrap as LEngineBootstrap
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum


class Helper():
    def __init__(self):
        self._lexicomb_ioc = None
        self._lexicomb_parser = None
        self._lexer = None
        self._logger = logging.getLogger('test_integration.helper')
        self.bootstrap()

    def bootstrap(self):
        app_config = {
            "logger": {
                "version": 1,
                "formatters": {
                    "detailed": {
                        "class": "logging.Formatter",
                        "format": "%(asctime)s [%(levelname)s] [%(name)s] [%(thread)d] [%(module)s::%(funcName)s] = %(message)s"
                    },
                    "context_detailed": {
                        "class": "logging.Formatter",
                        "format": "%(asctime)s [%(levelname)s] [%(name)s] [%(thread)d] [%(CONTEXT_ID)s] [%(module)s::%(funcName)s] %(message)s"
                    },
                    "standard": {
                        "class": "logging.Formatter",
                        "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s::%(funcName)s] %(message)s"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "standard"
                    }
                },
                "loggers": {
                    "bbpyp": {
                        "level": "ERROR",
                        "handlers": ["console"]
                    },
                    "test_integration": {
                        "level": "ERROR",
                        "handlers": ["console"]
                    }
                }
            },
            "memory_channel_max_buffer_size": 0,
            "lexicomb": {
                "lexicon": "test_integration/lexicomb/lexicon/"
            }
        }

        lexicomb_engine = LEngineBootstrap(app_config, lambda *args, **kwargs: None)

        self._lexicomb_ioc = lexicomb_engine.lexicomb_ioc
        self._lexicomb_parser = lexicomb_engine.lexicomb_ioc.parser_provider()
        self._lexer = lexicomb_engine.lexicomb_ioc.lexer_provider()
        self._result_factory = self._lexicomb_ioc.result_factory_provider

    def tokenize(self, input_line):
        return self._lexer.tokenize(input_line)

    def create_operator_enum(self, operator):
        return OperatorEnum(operator)

    @property
    def lexicomb_parser(self):
        return self._lexicomb_parser

    @property
    def lexicomb_ioc(self):
        return self._lexicomb_ioc

    @property
    def logger(self):
        return self._logger
