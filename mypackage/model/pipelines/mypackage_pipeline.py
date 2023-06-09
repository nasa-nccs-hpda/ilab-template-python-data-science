import logging


def run() -> None:
    logging.info('Execute pipeline "run" action')

    return


def setup() -> None:
    # Working on the setup of the project
    logging.info('Starting setup pipeline step')

    return


def _read_config(config_filename):
    return config_filename


class MyPackagePipeline(object):

    def __init__(self, config_filename, logger=None):
        # Set logger
        self.logger = logger if logger is not None else self._set_logger()

        # Configuration file initialization
        self.conf = _read_config(config_filename)
        logging.info(f'Init complete...')

    # -------------------------------------------------------------------------
    # setup
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # wrf
    # -------------------------------------------------------------------------

    def _set_logger(self):
        pass
