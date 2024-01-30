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
import requests
import re
import os
import apprise

# Set up the global logger variable
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
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

    parser.add_argument(
        "--configfile",
        default="mpad-watcher.yml",
        type=argparse.FileType("r"),
        help="MPAD Watcher config file",
    )

    args = parser.parse_args()
    mpad_watcher_ttl = args.ttl_alert_after
    mpad_watcher_configfile = args.configfile

    return mpad_watcher_ttl, mpad_watcher_configfile


def get_mpad_status_info(callsign: str = "MPAD"):
    """
    Gets MPAD's status info from aprs.fi, extracts
    the "last heard" timestamp from the JSON object
    and returns the timestamp as string

    Parameters
    ==========
    url: 'str'
        URL that we want to query

    Returns
    =======
    lasttime : 'float'
            'Last position' time stamp as float, 'None"
            in case of an error
    """

    resp = None
    # Default user agent which is used by the program for sending requests to aprs.fi
    default_user_agent = (
        f"mpad-watcher (+https://github.com/joergschultzelutter/mpad-watcher/)"
    )
    headers = {"User-Agent": default_user_agent}

    aprsdotfi_api_key = os.environ.get("MPAD_WATCHER_API_KEY")
    if not aprsdotfi_api_key:
        logger.debug(msg="aprs.fi API key environment variable is not set")
        return None

    # convert to upper if provided differently
    callsign = callsign.upper()

    try:
        resp = requests.get(
            url=f"https://api.aprs.fi/api/get?name={callsign}&what=loc&apikey={aprsdotfi_api_key}&format=json",
            headers=headers,
        )
    except Exception as ex:
        resp = None
    if resp:
        if resp.status_code == 200:
            try:
                json_content = resp.json()
            except Exception as ex:
                json_content = {}
            # extract web service result. Can either be 'ok' or 'fail'
            if "result" in json_content:
                result = json_content["result"]
            if result == "ok":
                # extract number of result sets in the response. Must be > 0
                # regardless of the available number of results, we will only
                # use the first result
                found = 0
                if "found" in json_content:
                    found = json_content["found"]
                if found > 0:
                    # We extract only the very first entry and disregard
                    # entries 2..n whereas ever present
                    # now extract lasttime
                    if "lasttime" in json_content["entries"][0]:
                        try:
                            return float(json_content["entries"][0]["lasttime"])
                        except ValueError:
                            pass
    return None


def does_file_exist(file_name: str):
    """
    Checks if the given file exists. Returns True/False.

    Parameters
    ==========
    file_name: str
                    our file name
    Returns
    =======
    status: bool
        True /False
    """
    return os.path.isfile(file_name)


def send_apprise_message(configfile: str, msg_title: str, msg_body: str):
    """
    Sends a message via Apprise (https://github.com/caronc/apprise)

    Parameters
    ==========
    configfile: str
        Apprise YML config file
    msg_title: str
        our message title
    msg_body: str
        our message body
    Returns
    =======
    status: bool
        True /False
    """

    if not does_file_exist(configfile):
        logger.debug(msg=f"Config file '{configfile}' does not exist")
        return False

    # Create the Apprise instance
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    config.add(configfile)

    # Make sure to add our config into our apprise object
    apobj.add(config)

    # Send the notification
    apobj.notify(
        body=msg_body,
        title=msg_title,
        tag="all",
    )

    return True


if __name__ == "__main__":
    send_apprise_message("mpad-watcher.yml", "Title", "Ich bin ein Body")
    pass
