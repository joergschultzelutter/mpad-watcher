# mpad-watcher

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Super-quick-and-dirty hack which checks on MacOS if my local MPAD instance is still running. In case of failure, a message notification will be dispatched to the user's local account via osascript / MacOS Message Center.

## Configuration
- clone repository
- copy `watcher.sh.TEMPLATE` to `watcher.sh`
- `chmod u+x watcher.sh`
- edit `watcher.sh`:
  - add your `aprs.fi` API key to variable `MPAD_WATCHER_API_KEY`
  - Check script assumes a program crash if (`systime` - `last heard on aprs.fi`) > 90 (minutes). You can change this value by specifying the `--ttl_alert_after` value in minutes
  - amend the path for the repo's location (`cd /path/to/mpad-watcher`)
  - save file
- open Apple's ScriptEditor
  - amend the path to the `watcher.sh` script
  - change the `timerInterval` value, if necessary. Default is 3600 secs = 60 min
  - save the script as is for further references
  - Then save the file as an application (`File` -> `Export` -> File Format: `Application`)
- In the Finder, locate the application that you have just created
- Right Mouse Button -> 'Show Package Contents'
- Edit `Contents/Info.plist`:

Your current Info.plist will look like this
```
	<key>CFBundleSignature</key>
	<string>aplt</string>
	<key>LSMinimumSystemVersionByArchitecture</key>
	<dict>
		<key>x86_64</key>
		<string>10.6</string>
	</dict>
	<key>LSRequiresCarbon</key>
	<true/>
```

Now add these two entries - this change will prevent the application from adding an icon to the MacOS dock: 

```
	<key>LSUIElement</key>
	<true/>
```

Final result will look like this:

```
	<key>CFBundleSignature</key>
	<string>aplt</string>
	<key>LSMinimumSystemVersionByArchitecture</key>
	<dict>
		<key>x86_64</key>
		<string>10.6</string>
	</dict>
	<key>LSRequiresCarbon</key>
	<true/>
	<key>LSUIElement</key>
	<true/>
```
- save the file
- END of configuration steps

## Running the application

- Double-click the application. If all works well (e.g. correct API key et al), you should not receive any message (but the application still keeps on running per MacOS's Activity monitor)\
- You can now add this application as a MacOS login item.