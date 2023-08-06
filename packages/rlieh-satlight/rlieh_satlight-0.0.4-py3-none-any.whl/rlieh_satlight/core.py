#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Olivier Watté <user>
# @Date:   2018-04-22T06:05:58-04:00
# @Email:  owatte@ipeos.com
# @Last modified by:   user
# @Last modified time: 2018-12-18T14:47:24-04:00
# @License: GPLv3
# @Copyright: IPEOS I-Solutions

import argparse
import configparser
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class RliehSatLight(object):
    """This class manage PWM on RLIEH sat using the web API.

    Attributes:
        ini_file_path (str) : full path to the .ini file
        light_phase (str): light phase

    """

    def __init__(self, ini_file_path, light_phase):
        """Retrieve parames from .ini and build api request."""

        self.ini_file_path = ini_file_path
        self.light_phase = light_phase

        # read config from .ini file
        config = configparser.ConfigParser()
        config.read(ini_file_path)

        # pwm light values
        limits = json.loads(config.get('light_thresholds', light_phase))
        start = limits[0]
        end = limits[1]
        duration = config['light_duration'][light_phase]

        # light IP
        ip = config['hardware']['ip']
        channel = config['hardware']['pwm_channel']

        # api version (temp param waiting for API harmonization)
        try:
            version = config['hardware']['version']
        except configparser.NoOptionError:
            version = 0
        except KeyError:
            version = 0

        if version == 0:
            self.endpoint = 'http://{}/api/pwms/{}'.format(ip, channel)
        else:
            self.endpoint = 'http://{}/pwms/{}'.format(ip, channel)

        # request payload
        self.payload = {
            'from': start,
            'to': end,
            'duration': duration
        }

    def requests_retry_session(self,
                               retries=3,
                               backoff_factor=0.3,
                               status_forcelist=(500, 502, 504),
                               session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def request(self):
        """performs API request."""
        # r = requests.put(self.endpoint, data=self.payload)
        r = self.requests_retry_session().put(self.endpoint, data=self.payload)

        if r.status_code == 200:
            return r.text
        else:
            raise ValueError('''could not manage light on {}.
            Returned message was
            {}'''.format(self.endpoint, self.light_phase))


def main():
    parser = argparse.ArgumentParser(description='Manage light on RLIEH sat.')
    parser.add_argument('-i', '--ini', help=".ini file path", required=True)
    parser.add_argument('-p', '--phase', help="light phase", required=True)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    args = parser.parse_args()

    light = RliehSatLight(args.ini, args.phase)
    r = light.request()
    if args.verbose:
        print(r)


if __name__ == "__main__":
    main()
