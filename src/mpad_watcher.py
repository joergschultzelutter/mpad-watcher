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
from utils import (
    get_command_line_params,
    convert_date_to_unix_timestamp,
    get_mpad_status_info,
)
import time

# Set up the global logger variable
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    ttl = get_command_line_params()

    website_str_timestamp = get_mpad_status_info()
    if website_str_timestamp:
        website_unix_timestamp = convert_date_to_unix_timestamp(
            date_string=website_str_timestamp
        )
        if website_unix_timestamp:
            system_unix_timestamp = time.time()
            seconds = system_unix_timestamp - website_unix_timestamp
            if seconds > (ttl * 60):
                logger.debug(msg="TTL exceeded")
                print(website_str_timestamp)
            else:
                print("OK")
        else:
            logger.debug(msg="Cannot convert website time stamp")
            print("ERROR - Cannot convert website time stamp")
    else:
        logger.debug(msg="Cannot retrieve website time stamp")
        print("ERROR - cannot retrieve website time stamp")
