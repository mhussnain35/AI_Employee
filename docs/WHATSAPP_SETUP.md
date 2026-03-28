# WhatsApp Web Setup Guide

This guide walks you through setting up WhatsApp Web monitoring for the AI Employee WhatsAppWatcher.

---

## Overview

The WhatsAppWatcher monitors WhatsApp Web for new messages containing urgent keywords. When it detects an urgent message, it creates an action file in the `Needs_Action/` folder for processing.

**Authentication Method:** QR Code scan (session-based)

---

## Prerequisites

### 1. Python Dependencies

Make sure Playwright is installed:

```bash
# Dependencies should already be installed via:
uv add playwright google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Install Chromium Browser

Playwright needs to install a browser:

```bash
playwright install chromium
```

**Time:** ~2 minutes (downloads ~100MB)

---

## Step 1: Create Session Directory

The session directory is created automatically, but you can create it manually:

```bash
mkdir sessions
mkdir sessions/whatsapp
```

**Time:** ~30 seconds

---

## Step 2: Authenticate with WhatsApp

Run the authentication script:

```bash
python main.py setup-whatsapp
```

Or directly:

```bash
python scripts/whatsapp_init.py
```

**What happens:**
1. A browser window will open showing WhatsApp Web
2. A QR code will appear
3. You have 2 minutes to scan it

**Time:** ~3 minutes

---

## Step 3: Scan QR Code with Phone

### On iPhone:
1. Open **WhatsApp** app
2. Go to **Settings** (gear icon)
3. Tap **Linked Devices**
4. Tap **Link a Device**
5. Point camera at QR code on screen

### On Android:
1. Open **WhatsApp** app
2. Tap **⋮** (three dots) → **Linked devices**
3. Tap **Link a device**
4. Point camera at QR code on screen

**What happens next:**
- Phone vibrates when QR code is scanned
- WhatsApp Web loads your chats
- Browser shows "Authentication successful"
- Session is saved to `sessions/whatsapp/`

---

## Step 4: Verify Authentication

After successful authentication, you should see:

```
✓ Authentication successful!
✓ Session is valid and authenticated

WhatsApp Authentication Complete!

Session saved to: sessions/whatsapp
This session will be used automatically by WhatsAppWatcher.
```

---

## Step 5: Start WhatsApp Watcher

```bash
python main.py watcher-whatsapp
```

Or start all watchers:

```bash
python main.py watcher-all
```

The watcher will:
- Check WhatsApp every 30 seconds (by default)
- Look for messages with urgent keywords
- Create action files in `Needs_Action/` folder
- Monitor keywords: `urgent`, `asap`, `invoice`, `payment`, `help`

---

## How It Works

### Session Persistence

- First time: Scan QR code
- Session saved to `sessions/whatsapp/`
- Next runs: Auto-login with saved session
- Session lasts several days (varies)

### Message Detection

The watcher looks for:
1. **Unread messages** (messages with unread badge)
2. **Keyword matches** (messages containing urgent words)

When detected:
- Creates markdown file in `Needs_Action/`
- Includes sender name, message text, timestamp
- Marks priority based on keywords

---

## Troubleshooting

### Error: "QR Code detected - Authentication required"

**Cause:** Session expired or not authenticated

**Solution:**
```bash
# Re-run authentication
python main.py setup-whatsapp
```

### Error: "Failed to start browser"

**Possible causes:**
- Playwright not installed
- Chromium not installed
- Port already in use

**Solution:**
```bash
# Install playwright browsers
playwright install chromium

# Try again
python main.py setup-whatsapp
```

### Error: "Timeout waiting for WhatsApp Web"

**Possible causes:**
- Slow internet connection
- WhatsApp Web down
- Browser blocked by firewall

**Solution:**
1. Check internet connection
2. Try opening [web.whatsapp.com](https://web.whatsapp.com) manually
3. Disable firewall temporarily
4. Re-run authentication

### Watcher not detecting messages

**Possible causes:**
- No unread messages
- Keywords not matching
- Session expired

**Solution:**
```bash
# Test session
python scripts/whatsapp_init.py

# Send yourself a test message with keyword "urgent"
# Then run watcher again
```

### Browser opens but shows blank page

**Solution:**
```bash
# Clear session and re-authenticate
rm -rf sessions/whatsapp/*  # Mac/Linux
rmdir /s /q sessions\whatsapp\*  # Windows

python main.py setup-whatsapp
```

---

## Configuration Options

### Change Check Interval

Edit the watcher in `main.py`:

```python
# Default: 30 seconds
whatsapp_watcher = WhatsAppWatcher(vault_path, check_interval=60)  # 1 minute
```

### Modify Keywords

Edit `watchers/whatsapp_watcher.py`:

```python
# Default keywords
DEFAULT_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help']

# Add more keywords
DEFAULT_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 'deadline']

# Or use environment variable (from .env)
# WHATSAPP_KEYWORDS=urgent,asap,invoice,payment,help,meeting
```

### Run in Headless Mode

For production (after session is saved):

```python
# In watchers/whatsapp_watcher.py
# Change headless=True for background operation
self.browser = playwright.chromium.launch_persistent_context(
    user_data_dir=str(self.session_dir),
    headless=True,  # Change to True for background
    # ...
)
```

---

## Security Notes

### Session Storage

- Session data stored in `sessions/whatsapp/`
- Excluded from Git (`.gitignore`)
- Contains authentication cookies
- **Do not share** this folder

### Privacy

The watcher:
- ✓ Reads message text
- ✓ Reads sender name
- ✓ Monitors chat list
- ✗ Cannot send messages
- ✗ Cannot delete messages
- ✗ Cannot access media (photos, videos)

### WhatsApp Terms of Service

**Important:** This uses WhatsApp Web automation. Be aware of:
- WhatsApp's [Terms of Service](https://www.whatsapp.com/legal/terms-of-service)
- Automated usage may violate terms
- Use at your own risk
- Consider using official WhatsApp Business API for production

---

## Session Management

### Check Session Status

```bash
# Run auth script (tests existing session)
python scripts/whatsapp_init.py
```

### Extend Session Life

- Use WhatsApp Web regularly on same browser
- Don't logout from WhatsApp Web
- Re-authenticate before session expires

### Revoke Session

On your phone:
1. WhatsApp → Settings → Linked Devices
2. Find "AI Employee" or the browser session
3. Tap **Logout**

### Backup Session

```bash
# Backup session folder
cp -r sessions/whatsapp sessions/whatsapp.backup

# Restore session
cp -r sessions/whatsapp.backup sessions/whatsapp
```

---

## Best Practices

1. **Regular Re-authentication:** Re-scan QR code every few days
2. **Monitor Logs:** Watch for "session expired" warnings
3. **Test Messages:** Send yourself test messages to verify detection
4. **Keyword Tuning:** Adjust keywords to reduce false positives
5. **Battery Impact:** Running browser continuously uses battery (consider cloud deployment)

---

## Performance

### Resource Usage

- **Memory:** ~200-300 MB (Chromium browser)
- **CPU:** <5% (idle monitoring)
- **Network:** Minimal (WhatsApp Web handles sync)

### Optimization Tips

1. Increase check interval for lower CPU usage
2. Run only when needed (not 24/7)
3. Use dedicated machine for always-on monitoring

---

## Alternative: WhatsApp Business API

For production use, consider official API:

- [WhatsApp Business Platform](https://business.whatsapp.com/)
- More reliable than Web automation
- Official support
- Requires business verification
- Costs per conversation

---

## Next Steps

After setting up WhatsApp:

1. ✓ Start WhatsApp watcher: `python main.py watcher-whatsapp`
2. ✓ Start all watchers: `python main.py watcher-all`
3. ✓ Send yourself a test message: "This is urgent!"
4. ✓ Check `Needs_Action/` folder for action file
5. ✓ Process items: `python main.py process`

---

## Support

If you encounter issues:

1. Check `sessions/whatsapp/` folder exists
2. Re-run `setup-whatsapp` script
3. Check WhatsApp Web works manually
4. Review logs in terminal output
5. Check Playwright installation: `playwright install chromium`

---

*Your AI Employee is now listening to WhatsApp! 📱*
