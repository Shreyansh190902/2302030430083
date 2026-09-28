#!/bin/bash
# Runs delta_sync.py every day at the time you choose (macOS launchd). If the Mac is asleep then, it runs when it wakes.
cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
LABEL="com.roadto1lakh.deltasync"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.delta_tracker"

read -r -p "What time should it save your Delta balance each day? (24-hour HH:MM) [23:30]: " T
[ -z "$T" ] && T="23:30"
H="${T%%:*}"; M="${T##*:}"
if ! [[ "$H" =~ ^[0-9]{1,2}$ && "$M" =~ ^[0-9]{1,2}$ ]] || [ "$H" -gt 23 ] || [ "$M" -gt 59 ]; then
  echo "That isn't a time like 23:30."; read -r -p "Press Return to close." _; exit 1
fi

cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$HERE/delta_sync.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>$((10#$H))</integer><key>Minute</key><integer>$((10#$M))</integer></dict>
  <key>StandardOutPath</key><string>$HOME/.delta_tracker/launchd.log</string>
  <key>StandardErrorPath</key><string>$HOME/.delta_tracker/launchd.log</string>
</dict>
</plist>
PL

launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1
launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null || launchctl load "$PLIST"
printf "Done. Your Delta balance will be saved to the tracker every day at %02d:%02d.\n" "$((10#$H))" "$((10#$M))"
echo "Weekends and NSE holidays are skipped. Keep the tracker closed in Excel at that time."
echo "To stop it later, double-click \"Uninstall Daily Sync.command\"."
read -r -p "Press Return to close." _
