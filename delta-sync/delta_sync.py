#!/usr/bin/env python3
"""Delta Exchange → Trading_PnL_Tracker.xlsx

Reads your Delta Exchange wallet balance (read-only API key) and writes it as the
day's Closing Balance (column H) in the Excel tracker. Standard library only.

Credentials come from the macOS Keychain (service "Delta Tracker", accounts
"api_key" and "api_secret"), stored there by Setup.command. For testing, the
environment variables DELTA_API_KEY / DELTA_API_SECRET override the Keychain.

Usage:
  python3 delta_sync.py              fill today's closing balance
  python3 delta_sync.py --show       only show the Delta balances (writes nothing)
  python3 delta_sync.py --date 2026-10-05   fill a specific trading day
  python3 delta_sync.py --dry-run    work everything out, but don't save the Excel file
"""
import argparse
import csv
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile

CONFIG_DIR = os.path.expanduser(os.environ.get("DELTA_TRACKER_HOME", "~/.delta_tracker"))
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
LOG_PATH = os.path.join(CONFIG_DIR, "sync.log")
HISTORY_PATH = os.path.join(CONFIG_DIR, "balances.csv")
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")
KEYCHAIN_SERVICE = "Delta Tracker"
DEFAULTS = {
    "excel_path": os.path.expanduser("~/Documents/Trading_PnL_Tracker.xlsx"),
    "base_url": "https://api.india.delta.exchange",
    "asset": "auto",            # "auto", "INR" or "USD"
    "balance_field": "balance",  # field of the wallet entry to use
    "usd_inr_rate": None,        # only needed if your wallet is in USD and Delta gives no INR figure
    "keep_backups": 30,
}
FIRST_ROW = 13      # Day 1 is on row 13 of the Tracker sheet
MAX_DAYS = 500
EXCEL_EPOCH = dt.date(1899, 12, 30)
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


class SyncError(Exception):
    pass


# ----------------------------------------------------------------- helpers
def log(msg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def notify(msg):
    if sys.platform == "darwin" and not os.environ.get("DELTA_TRACKER_NO_NOTIFY"):
        safe = msg.replace('"', "'")
        subprocess.run(["osascript", "-e", f'display notification "{safe}" with title "Delta Tracker"'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def load_config():
    cfg = dict(DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg.update(json.load(f))
    cfg["excel_path"] = os.path.expanduser(cfg["excel_path"])
    return cfg


def keychain_get(account):
    try:
        out = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", account, "-w"],
                             capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def credentials():
    key = os.environ.get("DELTA_API_KEY") or keychain_get("api_key")
    secret = os.environ.get("DELTA_API_SECRET") or keychain_get("api_secret")
    if not key or not secret:
        raise SyncError("No Delta API key found. Double-click Setup.command first.")
    return key, secret


# ----------------------------------------------------------------- Delta API
def signed_get(cfg, path, query=""):
    """GET a private Delta endpoint. Signature = HMAC-SHA256(secret, method + timestamp + path + query + body)."""
    key, secret = credentials()
    ts = str(int(time.time()))
    q = ("?" + query) if query else ""
    prehash = "GET" + ts + path + q + ""
    sig = hmac.new(secret.encode(), prehash.encode(), hashlib.sha256).hexdigest()
    req = urllib.request.Request(cfg["base_url"].rstrip("/") + path + q, headers={
        "api-key": key, "timestamp": ts, "signature": sig,
        "User-Agent": "delta-tracker-mac/1.0", "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:400]
        hint = ""
        if "ip" in body.lower() and "whitelist" in body.lower():
            hint = f" Your current internet IP isn't whitelisted on this API key. Add {public_ip() or 'your current IP'} in Delta → API Keys."
        elif e.code in (401, 403):
            hint = " Check the key/secret (run Setup.command again) and that the key's IP whitelist includes this Mac's IP."
        raise SyncError(f"Delta refused the request (HTTP {e.code}): {body}.{hint}")
    except urllib.error.URLError as e:
        raise SyncError(f"Couldn't reach Delta Exchange ({e.reason}). Are you online?")
    if not data.get("success", True):
        raise SyncError(f"Delta returned an error: {json.dumps(data.get('error', data))[:400]}")
    return data


def public_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=8) as r:
            return r.read().decode().strip()
    except Exception:
        return None


def wallet_entries(cfg):
    data = signed_get(cfg, "/v2/wallet/balances")
    result = data.get("result", data)
    if isinstance(result, dict):
        result = [result]
    return [x for x in result if isinstance(x, dict)]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def pick_balance(entries, cfg):
    """Return (balance_in_inr, description)."""
    field = cfg.get("balance_field") or "balance"
    by_asset = {str(e.get("asset_symbol") or e.get("asset", {}).get("symbol") or "").upper(): e for e in entries}
    want = (cfg.get("asset") or "auto").upper()
    order = ["INR", "USD"] if want == "AUTO" else [want]
    for sym in order:
        e = by_asset.get(sym)
        if not e:
            continue
        if sym == "INR" and num(e.get(field)) is not None:
            return round(num(e[field]), 2), f"INR wallet · {field}"
        # USD wallet: prefer an INR figure Delta already provides, else convert with your rate
        for k in (f"{field}_inr", "balance_inr", f"inr_{field}"):
            if num(e.get(k)) is not None:
                return round(num(e[k]), 2), f"USD wallet · {k} (Delta's INR figure)"
        if num(e.get(field)) is not None:
            rate = num(cfg.get("usd_inr_rate"))
            if not rate:
                raise SyncError(f"Your Delta wallet is in USD (${num(e[field]):,.2f}) and Delta didn't send an INR figure. "
                                "Run Setup.command again and enter the ₹-per-$ rate Delta uses (shown on its deposit page).")
            return round(num(e[field]) * rate, 2), f"USD wallet · {field} × ₹{rate}/$"
    raise SyncError("Couldn't find an INR or USD balance in your Delta wallet. Run: python3 delta_sync.py --show")


# ----------------------------------------------------------------- Excel (edited in place, keeps charts/formatting)
def sheet_paths(z):
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    targets = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship[^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"', rels)}
    targets.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship[^>]*?Target="([^"]+)"[^>]*?Id="([^"]+)"', rels)})
    out = {}
    for m in re.finditer(r'<sheet\b[^>]*?>', wb):
        tag = m.group(0)
        name = re.search(r'name="([^"]+)"', tag)
        rid = re.search(r'r:id="([^"]+)"', tag)
        if name and rid and rid.group(1) in targets:
            t = targets[rid.group(1)]
            out[unescape(name.group(1))] = t.lstrip("/") if t.startswith("/") else "xl/" + t
    return out


def unescape(s):
    return s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")


def cell_number(xml, ref):
    m = re.search(r'<c r="%s"(?:\s[^>]*)?>(.*?)</c>' % ref, xml, re.S)
    if not m:
        return None
    v = re.search(r"<v>([^<]*)</v>", m.group(1))
    return num(v.group(1)) if v else None


def cell_text(xml, ref, shared):
    m = re.search(r'<c r="%s"((?:\s[^>]*)?)>(.*?)</c>' % ref, xml, re.S)
    if not m:
        return ""
    attrs, body = m.group(1), m.group(2)
    if 't="s"' in attrs:
        v = re.search(r"<v>(\d+)</v>", body)
        return shared[int(v.group(1))] if v and int(v.group(1)) < len(shared) else ""
    return unescape("".join(re.findall(r"<t[^>]*>([^<]*)</t>", body)))


def shared_strings(z):
    try:
        xml = z.read("xl/sharedStrings.xml").decode("utf-8")
    except KeyError:
        return []
    return [unescape("".join(re.findall(r"<t[^>]*>([^<]*)</t>", si))) for si in re.findall(r"<si>(.*?)</si>", xml, re.S)]


def trading_days(start, holidays, until):
    """Trading dates from the first trading day on/after start, through `until`."""
    d, out = start, []
    while d <= until and len(out) < MAX_DAYS:
        if d.weekday() < 5 and d not in holidays:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


CELL_RE = r'<c r="{ref}"((?:\s+[\w:]+="[^"]*")*)\s*(?:/>|>(.*?)</c>)'


def set_cell(xml, ref, value):
    """Set a cell to a number (float) or inline string, keeping its style. The cell must exist."""
    pat = re.compile(CELL_RE.format(ref=ref), re.S)
    m = pat.search(xml)
    if not m:
        raise SyncError(f"Cell {ref} wasn't found in the Tracker sheet. Use the Trading_PnL_Tracker.xlsx template.")
    attrs = re.sub(r'\s+t="[^"]*"', "", m.group(1))
    if isinstance(value, (int, float)):
        new = f'<c r="{ref}"{attrs}><v>{repr(float(value)) if not float(value).is_integer() else int(value)}</v></c>'
    else:
        esc = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        new = f'<c r="{ref}"{attrs} t="inlineStr"><is><t xml:space="preserve">{esc}</t></is></c>'
    return xml[:m.start()] + new + xml[m.end():]


def drop_cached_results(xml):
    """Formula results cached in the file go stale when an input changes; remove them so the app recalculates."""
    def fix(m):
        attrs, body = m.group(1), m.group(2)
        if "<f" not in body:
            return m.group(0)
        attrs = re.sub(r'\s+t="[^"]*"', "", attrs)
        body = re.sub(r"<v>[^<]*</v>|<v/>", "", body)
        return f"<c{attrs}>{body}</c>"
    return re.sub(r"<c((?:\s+[\w:]+=\"[^\"]*\")*)>(.*?)</c>", fix, xml, flags=re.S)


def write_balance(cfg, when, balance, source, dry_run=False):
    path = cfg["excel_path"]
    if not os.path.exists(path):
        raise SyncError(f"Excel file not found: {path}. Run Setup.command and drag your tracker file in.")
    lock = os.path.join(os.path.dirname(path), "~$" + os.path.basename(path))
    if os.path.exists(lock):
        raise SyncError("The tracker is open in Excel. Close it and run the sync again (your balance wasn't written).")
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        files = {n: z.read(n) for n in names}
        infos = {i.filename: i for i in z.infolist()}
        sheets = sheet_paths(z)
        shared = shared_strings(z)
    if "Tracker" not in sheets:
        raise SyncError("This workbook has no 'Tracker' sheet. Use the Trading_PnL_Tracker.xlsx template.")
    tr = files[sheets["Tracker"]].decode("utf-8")
    header = cell_text(tr, "H12", shared)
    if "closing balance" not in header.lower():
        raise SyncError("This looks like an older tracker layout. Download a fresh Excel file from the dashboard.")
    start_serial = cell_number(tr, "C5")
    if start_serial is None:
        raise SyncError("Couldn't read the start date (Tracker!C5).")
    start = EXCEL_EPOCH + dt.timedelta(days=int(start_serial))
    holidays = set()
    if "NSE Holidays" in sheets:
        hx = files[sheets["NSE Holidays"]].decode("utf-8")
        for r in range(5, 65):
            v = cell_number(hx, f"A{r}")
            if v:
                holidays.add(EXCEL_EPOCH + dt.timedelta(days=int(v)))
    if when.weekday() >= 5 or when in holidays:
        return None, f"{when:%a %d %b %Y} isn't an NSE trading day (weekend or holiday), so nothing was written."
    days = trading_days(start, holidays, when)
    if not days or days[-1] != when:
        return None, f"{when:%d %b %Y} is before your tracker's first trading day ({start:%d %b %Y})."
    day = len(days)
    row = FIRST_ROW + day - 1
    tr = set_cell(tr, f"H{row}", balance)
    note_now = cell_text(tr, f"K{row}", shared)
    if not note_now:
        tr = set_cell(tr, f"K{row}", f"Delta sync {dt.datetime.now():%d %b %H:%M}")
    files[sheets["Tracker"]] = tr.encode("utf-8")
    for n in sheets.values():
        files[n] = drop_cached_results(files[n].decode("utf-8")).encode("utf-8")
    wb = files["xl/workbook.xml"].decode("utf-8")
    if "<calcPr" in wb:
        wb = re.sub(r"<calcPr\b([^>]*?)(/?)>", lambda m: "<calcPr" + re.sub(r'\s+fullCalcOnLoad="[^"]*"', "", m.group(1)) + ' fullCalcOnLoad="1"' + m.group(2) + ">", wb, count=1)
    else:
        wb = wb.replace("</sheets>", '</sheets><calcPr fullCalcOnLoad="1"/>', 1) if "<definedNames" not in wb else re.sub(r"(</definedNames>)", r'\1<calcPr fullCalcOnLoad="1"/>', wb, count=1)
    files["xl/workbook.xml"] = wb.encode("utf-8")
    if "xl/calcChain.xml" in files:   # stale calculation chain: remove it and its references
        del files["xl/calcChain.xml"]
        ct = files["[Content_Types].xml"].decode("utf-8")
        files["[Content_Types].xml"] = re.sub(r'<Override[^>]*PartName="/xl/calcChain.xml"[^>]*/>', "", ct).encode("utf-8")
        rels = files["xl/_rels/workbook.xml.rels"].decode("utf-8")
        files["xl/_rels/workbook.xml.rels"] = re.sub(r'<Relationship[^>]*Target="[^"]*calcChain.xml"[^>]*/>', "", rels).encode("utf-8")
    if dry_run:
        return day, f"[dry run] Would write ₹{balance:,.2f} to Day {day} ({when:%a %d %b %Y}, cell H{row})."
    # backup, then write atomically
    os.makedirs(BACKUP_DIR, exist_ok=True)
    shutil.copy2(path, os.path.join(BACKUP_DIR, f"{os.path.splitext(os.path.basename(path))[0]}-{dt.datetime.now():%Y%m%d-%H%M%S-%f}.xlsx"))
    backups = sorted(f for f in os.listdir(BACKUP_DIR) if f.endswith(".xlsx"))
    for old in backups[:-int(cfg.get("keep_backups") or 30)]:
        os.remove(os.path.join(BACKUP_DIR, old))
    fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=os.path.dirname(path))
    os.close(fd)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for n in names:
            if n in files:
                info = infos[n]
                zi = zipfile.ZipInfo(n, date_time=info.date_time)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = info.external_attr
                out.writestr(zi, files[n])
    os.replace(tmp, path)
    with open(HISTORY_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([when.isoformat(), day, f"{balance:.2f}", source, dt.datetime.now().isoformat(timespec="seconds")])
    return day, f"Wrote ₹{balance:,.2f} to Day {day} ({when:%a %d %b %Y}) in {os.path.basename(path)}."


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Copy your Delta Exchange balance into the Excel tracker.")
    ap.add_argument("--show", action="store_true", help="only show Delta wallet balances")
    ap.add_argument("--date", help="trading day to fill (YYYY-MM-DD); default today")
    ap.add_argument("--dry-run", action="store_true", help="don't save the Excel file")
    a = ap.parse_args()
    cfg = load_config()
    try:
        entries = wallet_entries(cfg)
        if a.show:
            print("Delta wallet balances:")
            for e in entries:
                sym = e.get("asset_symbol") or e.get("asset", {}).get("symbol")
                fields = {k: v for k, v in e.items() if isinstance(v, (str, int, float)) and ("balance" in k or "equity" in k or "margin" in k)}
                print(f"  {sym}: " + ", ".join(f"{k}={v}" for k, v in fields.items()))
            try:
                bal, how = pick_balance(entries, cfg)
                print(f"\nThe tracker would record: ₹{bal:,.2f}  ({how})")
            except SyncError as e:
                print(f"\n{e}")
            return 0
        bal, how = pick_balance(entries, cfg)
        if a.date:
            when = dt.date.fromisoformat(a.date)
        else:
            now = dt.datetime.now()
            # a run between midnight and 6 am (e.g. the Mac was asleep at the scheduled time) belongs to yesterday
            when = (now - dt.timedelta(days=1)).date() if now.hour < 6 else now.date()
        day, msg = write_balance(cfg, when, bal, how, dry_run=a.dry_run)
        log(msg + (f"  [{how}]" if day else ""))
        if day and not a.dry_run:
            notify(f"Day {day}: ₹{bal:,.2f} saved to your tracker")
        return 0
    except SyncError as e:
        log("ERROR: " + str(e))
        notify("Sync failed: " + str(e)[:120])
        return 2


if __name__ == "__main__":
    sys.exit(main())
