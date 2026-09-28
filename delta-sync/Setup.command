#!/bin/bash
# Delta Tracker setup: saves your Delta API key in the macOS Keychain and points the sync at your Excel file.
cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
CONF_DIR="$HOME/.delta_tracker"
SERVICE="Delta Tracker"
mkdir -p "$CONF_DIR"

echo "========================================"
echo "  Delta Exchange → Excel tracker setup"
echo "========================================"
echo

if ! /usr/bin/python3 --version >/dev/null 2>&1; then
  echo "Python 3 isn't installed yet. macOS will offer to install the Command Line Tools — click Install,"
  echo "wait for it to finish, then double-click Setup.command again."
  xcode-select --install 2>/dev/null
  read -r -p "Press Return to close." _
  exit 1
fi

echo "Step 1 of 4 — Delta API key"
echo "  Create a READ-ONLY key on Delta Exchange India (Account → API Keys):"
echo "  tick only \"Read Data\" — no trading, no withdrawals — and whitelist this Mac's IP."
IP="$(curl -s --max-time 8 https://api.ipify.org)"
[ -n "$IP" ] && echo "  This Mac's public IP right now: $IP"
echo
read -r -p "Paste your API key and press Return: " API_KEY
API_KEY="$(echo "$API_KEY" | tr -d '[:space:]')"
if [ -z "$API_KEY" ]; then echo "No key entered. Nothing was saved."; read -r -p "Press Return to close." _; exit 1; fi
read -r -s -p "Paste your API secret (it stays hidden) and press Return: " API_SECRET; echo
API_SECRET="$(echo "$API_SECRET" | tr -d '[:space:]')"
if [ -z "$API_SECRET" ]; then echo "No secret entered. Nothing was saved."; read -r -p "Press Return to close." _; exit 1; fi
security delete-generic-password -s "$SERVICE" -a api_key >/dev/null 2>&1
security delete-generic-password -s "$SERVICE" -a api_secret >/dev/null 2>&1
security add-generic-password -s "$SERVICE" -a api_key -w "$API_KEY" -T /usr/bin/security
security add-generic-password -s "$SERVICE" -a api_secret -w "$API_SECRET" -T /usr/bin/security
unset API_SECRET
echo "  Saved in your Keychain (entry \"$SERVICE\")."
echo

echo "Step 2 of 4 — Your Excel tracker"
DEFAULT_XLSX="$HOME/Documents/Trading_PnL_Tracker.xlsx"
echo "  Drag your Trading_PnL_Tracker.xlsx file into this window and press Return."
read -r -p "  (or just press Return for $DEFAULT_XLSX): " XLSX
XLSX="${XLSX%\"}"; XLSX="${XLSX#\"}"; XLSX="${XLSX%\'}"; XLSX="${XLSX#\'}"
XLSX="$(echo "$XLSX" | sed -e 's/\\ / /g' -e 's/[[:space:]]*$//')"
[ -z "$XLSX" ] && XLSX="$DEFAULT_XLSX"
if [ ! -f "$XLSX" ]; then
  echo "  Couldn't find that file. Put Trading_PnL_Tracker.xlsx in Documents (or drag it in) and run setup again."
  read -r -p "Press Return to close." _; exit 1
fi
echo

echo "Step 3 of 4 — Which Delta?"
read -r -p "  Delta Exchange India (1) or Delta Exchange global (2)? [1]: " WHICH
if [ "$WHICH" = "2" ]; then BASE="https://api.delta.exchange"; else BASE="https://api.india.delta.exchange"; fi

/usr/bin/python3 - "$CONF_DIR/config.json" "$XLSX" "$BASE" <<'PY'
import json, os, sys
path, xlsx, base = sys.argv[1:4]
cfg = {}
if os.path.exists(path):
    cfg = json.load(open(path))
cfg.update({"excel_path": xlsx, "base_url": base})
json.dump(cfg, open(path, "w"), indent=2)
PY
echo

echo "Step 4 of 4 — Test connection"
cd "$HERE" || exit 1
OUT="$(/usr/bin/python3 delta_sync.py --show 2>&1)"
echo "$OUT"
if echo "$OUT" | grep -q "Delta wallet is in USD"; then
  echo
  read -r -p "  Enter the ₹ per \$1 rate Delta uses (from its deposit page), e.g. 85: " RATE
  /usr/bin/python3 - "$CONF_DIR/config.json" "$RATE" <<'PY'
import json, sys
path, rate = sys.argv[1:3]
cfg = json.load(open(path)); cfg["usd_inr_rate"] = float(rate); json.dump(cfg, open(path, "w"), indent=2)
PY
  /usr/bin/python3 delta_sync.py --show
fi
echo
echo "Setup done. Next: double-click \"Install Daily Sync.command\" to run it every evening,"
echo "or run \"Sync Now.command\" any time."
read -r -p "Press Return to close." _
