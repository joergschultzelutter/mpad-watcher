#!/opt/local/bin/python3
#
# mpad-watcher
# Quick-and-dirty 'mpad' watchdog; generates output
# for the AppleScript watchdog
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

from utils import (
    get_command_line_params,
    get_mpad_status_info,
)
import time

if __name__ == "__main__":
    ttl = get_command_line_params()

    website_unix_timestamp = get_mpad_status_info()
    if website_unix_timestamp:
        system_unix_timestamp = time.time()
        seconds = system_unix_timestamp - website_unix_timestamp
        if seconds > (ttl * 60):
            print(f"ERROR - TTL exceeded; last heard: {website_str_timestamp}")
        else:
            print("OK")
    else:
        print("ERROR - cannot retrieve time stamp from aprs.fi")
