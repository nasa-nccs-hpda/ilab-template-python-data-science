import sys
import time
import logging
import argparse
from datetime import date
from wildfire_occurrence.model.common import valid_date
from wildfire_occurrence.model.pipelines.wrf_pipeline import WRFPipeline


# -----------------------------------------------------------------------------
# main
#
# python wrf_pipeline_cli.py -c config.yaml -sd 2023-04-05 \
#   -ed 2023-04-05 -s all
# -----------------------------------------------------------------------------
def main():

    # Process command-line args.
    desc = 'Use this application to perform CNN regression.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-c',
                        '--config-file',
                        type=str,
                        required=True,
                        dest='config_file',
                        help='Path to the configuration file')

    parser.add_argument('-d',
                        '--start-date',
                        type=valid_date,
                        required=False,
                        default=date.today(),
                        dest='start_date',
                        help='Start date for WRF')

    parser.add_argument('-l',
                        '--forecast-lenght',
                        type=int,
                        required=False,
                        default=10,
                        dest='forecast_lenght',
                        help='Lenght of WRF forecast')

    parser.add_argument(
                        '-s',
                        '--pipeline-step',
                        type=str,
                        nargs='*',
                        required=True,
                        dest='pipeline_step',
                        help='Pipeline step to perform',
                        default=[
                            'setup', 'geogrid', 'ungrib', 'metgrid',
                            'real', 'wrf', 'all'],
                        choices=[
                            'setup', 'geogrid', 'ungrib', 'metgrid',
                            'real', 'wrf', 'all'])

    args = parser.parse_args()

    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s; %(levelname)s; %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Setup timer to monitor script execution time
    timer = time.time()

    # Initialize pipeline object
    pipeline = WRFPipeline(
        args.config_file, args.start_date, args.forecast_lenght)

    # WRF pipeline steps
    if "setup" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.setup()
    if "geogrid" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.geogrid()
    if "ungrib" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.ungrib()
    if "metgrid" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.metgrid()
    if "real" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.real()
    if "wrf" in args.pipeline_step or "all" in args.pipeline_step:
        pipeline.wrf()

    logging.info(f'Took {(time.time()-timer)/60.0:.2f} min.')


# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
