# Delta Exchange → Excel tracker (Mac)

Saves your Delta Exchange wallet balance as the day's **Closing Balance** in `Trading_PnL_Tracker.xlsx`, automatically, every evening. Nothing to install beyond what macOS already has.

## 1. Create a read-only API key on Delta Exchange India

1. Log in to Delta Exchange India → **Account → API Keys → Create new API key**.
2. Permissions: tick **Read Data only**. Do **not** tick Trading or Withdrawals.
3. **Whitelist your IP**: `Setup.command` shows this Mac's current public IP. Add it on Delta.
4. Copy the **API key** and **API secret**. Don't send them to anyone, including in chat.

## 2. Set up (once)

1. Unzip `delta-sync.zip` and put the folder somewhere permanent, e.g. **Documents**.
2. Put your tracker at `Documents/Trading_PnL_Tracker.xlsx` (or drag it in during setup).
3. **Right-click `Setup.command` → Open → Open.** macOS asks the first time because the file came from the internet.
4. Paste the API key, then the API secret. The secret stays hidden, and both are saved in your **Keychain**, not in a file.
5. Setup tests the connection and shows your Delta balance.

## 3. Turn on the daily sync

Right-click **`Install Daily Sync.command` → Open**, and choose a time (default **23:30**).
Every day at that time your balance goes into that day's row. Weekends and NSE holidays are skipped.
If the Mac is asleep at that time, it runs when the Mac wakes. Runs between midnight and 6 am count for the previous day.

- **Sync Now.command** saves the balance right now.
- **Uninstall Daily Sync.command** stops the daily sync, and can delete the key from your Keychain.

## Using it with the website

After a sync, open the dashboard → **More → Import from Excel** and pick the tracker file. The website then has the same days.

## Good to know

- **Close the tracker in Excel** at sync time. If it's open, the sync stops and tells you, rather than risking your file.
- A **backup** of your tracker is saved before every write in `~/.delta_tracker/backups` (last 30 kept).
- A history of every saved balance is in `~/.delta_tracker/balances.csv`, and a log in `~/.delta_tracker/sync.log`.
- The sync writes a note like "Delta sync 05 Oct 23:30" in the Notes column, unless you already wrote a note there.
- **Home IP changes** (often about weekly): if the sync fails with an IP/whitelist error, add your new IP on Delta. `Setup.command` shows it.
- **USD wallet:** if Delta gives your balance in USD with no ₹ figure, setup asks for the ₹-per-$ rate Delta uses and converts with it.
- To see exactly what Delta returns: open Terminal in this folder and run `python3 delta_sync.py --show`.
