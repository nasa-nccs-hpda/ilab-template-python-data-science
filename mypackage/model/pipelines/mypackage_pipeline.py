import logging


class MyPackagePipeline(object):

    def __init__(
                self,
                config_filename: str,
                start_date: str,
                forecast_lenght: str,
            ):

        logging.info(f'Created output directory {self.simulation_dir}')


    # -------------------------------------------------------------------------
    # setup
    # -------------------------------------------------------------------------
    def setup(self) -> None:

        # Working on the setup of the project
        logging.info('Starting setup pipeline step')

        return


    # -------------------------------------------------------------------------
    # wrf
    # -------------------------------------------------------------------------
    def run(self) -> None:

        logging.info('Execute pipeline "run" action')

        return


