#!/bin/bash
# Stops the daily Delta sync. Optionally removes the saved API key from the Keychain.
LABEL="com.roadto1lakh.deltasync"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || launchctl unload "$PLIST" >/dev/null 2>&1
rm -f "$PLIST"
echo "Daily sync stopped."
read -r -p "Also delete your Delta API key from the Keychain? (y/N): " YN
if [ "$YN" = "y" ] || [ "$YN" = "Y" ]; then
  security delete-generic-password -s "Delta Tracker" -a api_key >/dev/null 2>&1
  security delete-generic-password -s "Delta Tracker" -a api_secret >/dev/null 2>&1
  echo "API key deleted. Also delete the key on Delta Exchange (Account → API Keys)."
fi
read -r -p "Press Return to close." _
