# Silver Tier - Quick Start Guide

## Installation Complete! ✓

Your AI Employee Silver Tier has been successfully implemented. Follow these steps to get started.

---

## Step 1: Wait for Dependencies to Install

The UV package manager is currently downloading dependencies. This may take 5-10 minutes depending on your internet speed.

**What's being installed:**
- `google-api-python-client` - Gmail API (~14 MB)
- `playwright` - Browser automation (~35 MB)
- Chromium browser - For WhatsApp (~100-200 MB)

**Check installation status:**
```bash
python -c "import google; print('Google:', 'OK')"
python -c "from playwright.sync_api import sync_playwright; print('Playwright:', 'OK')"
```

---

## Step 2: Install Playwright Browsers

After dependencies are installed, install the Chromium browser:

```bash
playwright install chromium
```

This downloads the Chromium browser (~100-200 MB) needed for WhatsApp Web automation.

---

## Step 3: Setup Gmail Authentication

### 3.1 Get Gmail Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Gmail API**
4. Create **OAuth2 credentials** (Desktop app)
5. Download `credentials.json`
6. Place it in the `credentials/` folder:
   ```
   AI_Employee/
   └── credentials/
       └── credentials.json  ← Place here
   ```

### 3.2 Run Authentication

```bash
python main.py setup-gmail
```

A browser window will open:
1. Sign in with your Google account
2. Grant permissions (read-only Gmail access)
3. Token saved automatically

**Success:** You should see "✓ All checks passed!"

---

## Step 4: Setup WhatsApp Authentication

```bash
python main.py setup-whatsapp
```

A browser window will open with WhatsApp Web:

1. Open WhatsApp on your phone
2. Go to **Settings** → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code on your screen

**Success:** Session saved to `sessions/whatsapp/`

**Note:** Session lasts several days. Re-authenticate when expired.

---

## Step 5: Start All Watchers

```bash
python main.py watcher-all
```

This starts all three watchers in parallel:
- **FileSystemWatcher** (checks every 5s)
- **GmailWatcher** (checks every 120s)
- **WhatsAppWatcher** (checks every 30s)

**Expected output:**
```
✓ All watchers started
Monitoring for new items...
```

**Stop watchers:** Press `Ctrl+C`

---

## Step 6: Test the System

### Test File System Watcher
1. Create a file: `AI_Employee_Vault/Inbox/test.txt`
2. Check: `AI_Employee_Vault/Needs_Action/`
3. An action file should appear within 5 seconds

### Test Gmail Watcher
1. Send yourself an email from another account
2. Mark it as **Important**
3. Wait up to 2 minutes
4. Check: `AI_Employee_Vault/Needs_Action/`

### Test WhatsApp Watcher
1. Send yourself a WhatsApp message with keyword "urgent"
2. Wait up to 30 seconds
3. Check: `AI_Employee_Vault/Needs_Action/`

---

## Step 7: Process Items

```bash
python main.py process
```

This processes all items in `Needs_Action/`:
- Reads action files
- Creates plans in `Plans/`
- Follows Company Handbook rules
- Moves completed items to `Done/`

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `python main.py` | Show help and status |
| `python main.py setup` | Initialize vault structure |
| `python main.py setup-gmail` | Authenticate with Gmail |
| `python main.py setup-whatsapp` | Authenticate with WhatsApp |
| `python main.py watcher` | Start file system watcher |
| `python main.py watcher-gmail` | Start Gmail watcher |
| `python main.py watcher-whatsapp` | Start WhatsApp watcher |
| `python main.py watcher-all` | Start all watchers |
| `python main.py process` | Process pending items |
| `python main.py status` | Show vault status |

---

## Troubleshooting

### Dependencies Not Installed

**Error:** `ModuleNotFoundError: No module named 'google'`

**Solution:**
```bash
uv sync
playwright install chromium
```

### Gmail Authentication Failed

**Error:** "credentials.json not found"

**Solution:**
1. Download from Google Cloud Console
2. Place in `credentials/credentials.json`
3. Run `python main.py setup-gmail` again

### WhatsApp Session Expired

**Error:** "QR Code detected - Authentication required"

**Solution:**
```bash
python main.py setup-whatsapp
```

### Watchers Not Detecting Items

**Check:**
1. Watchers are running (`python main.py watcher-all`)
2. Emails are marked as **unread** and **important**
3. WhatsApp messages contain keywords
4. Check terminal logs for errors

---

## Project Structure

```
AI_Employee/
├── main.py                    # Main CLI
├── watchers/                  # Watcher modules
│   ├── filesystem_watcher.py  # File monitoring
│   ├── gmail_watcher.py       # Gmail API
│   └── whatsapp_watcher.py    # WhatsApp Web
├── scripts/                   # Setup scripts
│   ├── gmail_auth.py          # Gmail OAuth2
│   └── whatsapp_init.py       # WhatsApp QR
├── AI_Employee_Vault/         # Obsidian vault
│   ├── Inbox/                 # Drop folder
│   ├── Needs_Action/          # Pending items
│   └── Plans/                 # Action plans
├── credentials/               # Gmail credentials
└── sessions/                  # WhatsApp sessions
```

---

## Next Steps

### Daily Usage

1. **Morning:** Start watchers
   ```bash
   python main.py watcher-all
   ```

2. **During Day:** Drop files in `Inbox/`, emails arrive, WhatsApp messages come in

3. **Evening:** Process items
   ```bash
   python main.py process
   ```

4. **Review:** Check `Needs_Action/` and `Pending_Approval/`

### Weekly Tasks

1. **Review Dashboard:** Open `AI_Employee_Vault/Dashboard.md` in Obsidian
2. **Check Plans:** Review `Plans/` folder for completed actions
3. **Audit:** Check `Briefings/` for weekly summaries (Gold Tier feature)

---

## Documentation

- **README.md** - Main project documentation
- **SECURITY.md** - Security and API keys guide
- **docs/GMAIL_SETUP.md** - Detailed Gmail setup
- **docs/WHATSAPP_SETUP.md** - Detailed WhatsApp setup
- **SILVER_TIER_SUMMARY.md** - Implementation summary

---

## Support

If you encounter issues:

1. Check logs in terminal output
2. Review setup guides in `docs/` folder
3. Re-run authentication scripts
4. Check credentials and sessions folders

---

*Your AI Employee is ready to work 24/7! 🎉*
