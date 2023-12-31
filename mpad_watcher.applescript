#
# mpad-watcher AppleScript
# Author: Joerg Schultze-Lutter, 2023
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#

# Amend path if necessary
set watcherScriptPath to "/Users/jsl/git/mpad-watcher/watcher.sh"
set timerInterval to 60 * 60

display notification "Checking mpad status every 60 minutes" with title "mpad-watcher"

repeat while true
	set batchscript_output to do shell script watcherScriptPath
	if batchscript_output is not equal to "OK" then
		display notification batchscript_output with title "mpad-watcher"
	end if
	delay timerInterval
end repeat