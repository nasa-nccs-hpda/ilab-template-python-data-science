import os
import re
import sys
import logging
import requests
import datetime
import pandas as pd
from datetime import date
from typing import List, Literal
from multiprocessing import Pool, cpu_count

__data_source__ = 'https://rda.ucar.edu/datasets/ds083.2'


class NCEP_FNL(object):

    def __init__(
                self,
                output_dir: str,
                start_date: str = date.today(),
                end_date: str = date.today(),
                hour_intervals: List = ['00', '06', '12', '18'],
                n_procs: int = cpu_count()
            ):

        # output directory
        self.output_dir = output_dir

        # define start and end data of download
        if isinstance(start_date, str):
            self.start_date = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()
        else:
            self.start_date = start_date

        # define start and end data of download
        if isinstance(end_date, str):
            self.end_date = datetime.datetime.strptime(
                end_date, '%Y-%m-%d').date()
        else:
            self.end_date = end_date

        # define hour intervals
        self.hour_intervals = hour_intervals

        # TODO: IF WE ARE DOWNLOADING INTO THE FUTURE
        # THEN WE NEED TO SPECIFY THIS IS FROM THE OTHER
        # DATASET AND NOT FROM THE CURRENT GFS

        # make sure we do not download data into the future
        # if self.end_date > datetime.datetime.now():
        #    self.end_date = datetime.datetime.now()
        #    self.hour_intervals = [
        #        d for d in self.hour_intervals
        #        if int(d) <= self.end_date.hour - 6]
        logging.info(
            f'Downloading data from {self.start_date} to {self.end_date}')

        # check for email and password environment variables
        if "NCEP_FNL_EMAIL" not in os.environ \
                or "NCEP_FNL_KEY" not in os.environ:
            sys.exit(
                "ERROR: You need to set NCEP_FNL_EMAIL and NCEP_FNL_KEY " +
                "to enable data downloads. If you do not have an " +
                "account, go to https://rda.ucar.edu/ and create one."
            )

        # define email and password fields
        self.email = os.environ['NCEP_FNL_EMAIL']
        assert re.search(r'[\w.]+\@[\w.]+', self.email), \
            f'{self.email} is not a valid email.'

        self.password = os.environ['NCEP_FNL_KEY']

        # define cookie filename to store auth
        self.cookie_filename = f'/home/{os.environ["USER"]}/.ncep_cookie'

        # define login url
        self.auth_url = 'https://rda.ucar.edu/cgi-bin/login'
        self.auth_request = {
            'email': self.email,
            'passwd': self.password,
            'action': 'login'
        }

        # define data url
        self.data_url = 'https://rda.ucar.edu'

        if self.start_date.year < 2008:
            self.grib_format = 'grib1'
        else:
            self.grib_format = 'grib2'

        self.dataset_path = f'/data/OS/ds083.2/{self.grib_format}'

        # nnumber of processors to use
        self.n_procs = n_procs

    def _authenticate(self, action: Literal["auth", "cleanup"] = "auth"):

        if action == "cleanup":
            # cleanup cookie filename
            os.remove(self.cookie_filename)
        else:
            # attempt to authenticate
            ret = requests.post(self.auth_url, data=self.auth_request)
            if ret.status_code != 200:
                sys.exit('Bad Authentication. Check email and password.')

            logging.info('Authenticated')

            os.system(
                f'wget --save-cookies {self.cookie_filename} ' +
                '--delete-after --no-verbose ' +
                f'--post-data="email={self.email}&' +
                f'passwd={self.password}&action=login" {self.auth_url}'
            )
        return

    def _download_file(self, wget_request: str):
        logging.info(wget_request)
        os.system(wget_request)
        return

    def download(self):

        # authenticate against NCEP
        self._authenticate(action="auth")

        # get list of filenames to download
        filenames = self._get_filenames()

        # setup list for parallel downloads
        download_requests = []
        for filename in filenames:

            # get year from the filename
            year = re.search(r'\d{4}', filename).group(0)

            # set full output directory and create it
            output_dir = os.path.join(self.output_dir, year)
            os.makedirs(output_dir, exist_ok=True)

            # set full url and output filename
            full_url = self.data_url + filename
            output_filename = os.path.join(
                output_dir, os.path.basename(filename))
            logging.info(f'Downloading {full_url} to {output_filename}')

            # download request for parallel download
            if not os.path.isfile(output_filename) or \
                    os.path.getsize(output_filename) == 0:
                download_requests.append(
                    f'wget --load-cookies {self.cookie_filename} ' +
                    f'--no-verbose -O {output_filename} {full_url}'
                )

        # Set pool, start parallel multiprocessing
        p = Pool(processes=self.n_procs)
        p.map(self._download_file, download_requests)
        p.close()
        p.join()

        # authenticate against NCEP
        self._authenticate(action="cleanup")

        return

    def _get_filenames(self):
        filenames_list = []
        daterange = pd.date_range(self.start_date, self.end_date)
        for single_date in daterange:
            year = single_date.strftime("%Y")
            for hour in self.hour_intervals:
                filename = os.path.join(
                    self.dataset_path,
                    f'{year}/{single_date.strftime("%Y.%m")}',
                    f'fnl_{single_date.strftime("%Y%m%d")}_' +
                    f'{hour}_00.{self.grib_format}'
                )
                filenames_list.append(filename)
        return filenames_list


# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    dates = [
        '2003-06-23',
        '2005-06-11',
        '2023-06-04'
    ]

    for init_date in dates:

        start_date = datetime.datetime.strptime(init_date, "%Y-%m-%d")
        end_date = (start_date + datetime.timedelta(days=10))

        downloader = NCEP_FNL(
            output_dir='output/NCEP_FNL',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        downloader.download()
