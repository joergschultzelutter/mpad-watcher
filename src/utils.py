#!/opt/local/bin/python3
#
# mpad-watcher
# Module: various utility functions used by the program
# Author: Joerg Schultze-Lutter, 2023
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import logging
import argparse
import datetime
import time
import requests
import re

# Set up the global logger variable
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


def get_command_line_params():
    """
    Get the command line params
    and returns information as a dictionary

    Parameters
    ==========

    Returns
    =======
    mpad_watcher_ttl : 'int'
            Number of minutes which will cause an alert if
            exceeded via (systime - last_heard_on_website)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ttl_alert_after",
        default=90,
        type=int,
        help="TTL check value in minutes",
    )

    args = parser.parse_args()
    mpad_watcher_ttl = args.ttl_alert_after

    return mpad_watcher_ttl


def convert_date_to_unix_timestamp(date_string: str):
    """
    Convert web site date-time-stamp to unix timestamp

    Parameters
    ==========
    date_string: 'str'
    Our imput date time stamp, including time zone

    Returns
    =======
    timestamp : 'float'
            Unix timestamp in case of a successful conversion,
            otherwise 'None'
    """

    try:
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S %Z")
        timestamp = time.mktime(date_object.timetuple())
        return timestamp
    except ValueError as e:
        logger.debug(msg=f"Error converting date string '{date_string}': {e}")
        return None


def get_mpad_status_info(url: str = "https://aprs.fi/info/a/MPAD"):
    """
    Gets MPAD's status page from aprs.fi, extracts
    the "last heard" timestamp from the HTML content
    and returns the timestamp as string

    Parameters
    ==========
    url: 'str'
        URL that we want to query

    Returns
    =======
    resp : 'str'
            'Last position' time stamp as string, 'None"
            in case of an error
    """

    resp = None
    try:
        resp = requests.get(url=url)
    except Exception as ex:
        logger.debug(msg=f"Cannot retrieve MPAD status page '{url}' from aprs.fi")
        resp = None

    if resp:
        if resp.status_code == 200:
            response = resp.text
            matches = re.search(
                pattern=r"\bLast position(.+)(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w+)",
                string=response,
                flags=re.IGNORECASE,
            )
            if matches:
                try:
                    resp = matches[2]
                except IndexError:
                    logger.debug(msg="Error while retrieving value from regex")
                    resp = None
    return resp


if __name__ == "__main__":
    pass
