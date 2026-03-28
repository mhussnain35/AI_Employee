# Chrome Browser Configuration ✓

## Updated: Both Gmail and WhatsApp Now Use Chrome

Both authentication scripts have been updated to **open Google Chrome by default**.

---

## What Changed

### Gmail Authentication (`scripts/gmail_auth.py`)

**Before:**
```
This will open a browser window.
```

**After:**
```
This will open Chrome browser.
Starting Chrome browser...
```

**Implementation:**
```python
# Tries to use Chrome specifically
chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab('about:blank')
```

---

### WhatsApp Authentication (`scripts/whatsapp_init.py`)

**Before:**
```
This will open a browser window with WhatsApp Web.
```

**After:**
```
This will open Chrome browser with WhatsApp Web.
Waiting for Chrome to open...
```

**Implementation:**
```python
# Launch Chrome browser with persistent context
browser = playwright.chromium.launch_persistent_context(
    user_data_dir=str(WHATSAPP_SESSION_DIR),
    headless=False,
    channel='chrome',  # Use Google Chrome specifically
    args=[...],
    timeout=60000
)
```

---

## Commands

### Gmail Authentication

```bash
python main.py setup-gmail
```

**Output:**
```
Starting Gmail OAuth2 Authentication
This will open Chrome browser.
IMPORTANT: If you see 'This app isn't verified':
  1. Click 'Advanced'
  2. Click 'Go to AI Employee (unsafe)'
  3. Click 'Allow' to grant permissions

Starting Chrome browser...
```

---

### WhatsApp Authentication

```bash
python main.py setup-whatsapp
```

**Output:**
```
WhatsApp Web Authentication
This will open Chrome browser with WhatsApp Web.

Steps to authenticate:
1. Wait for the QR code to appear
2. Open WhatsApp on your phone
3. Go to Settings → Linked Devices
4. Tap 'Link a Device'
5. Scan the QR code shown in the browser

Waiting for Chrome to open...
```

---

## Requirements

### Chrome Must Be Installed

**Check if Chrome is installed:**

```bash
# Windows Command Prompt
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**If Chrome is not installed:**

1. Download from: https://www.google.com/chrome/
2. Install Chrome
3. Authentication scripts will automatically use Chrome

---

## Fallback Behavior

If Chrome is not found, the scripts will:

- **Gmail:** Use the system default browser
- **WhatsApp:** Show an error message with instructions

**Error message:**
```
✗ Error during authentication: Chrome not installed
Common issues:
  1. Chrome not installed - install Google Chrome browser
```

---

## Why Chrome?

1. **Consistency:** Same browser for both Gmail and WhatsApp
2. **Reliability:** Chrome works best with Google services
3. **WhatsApp Web:** Officially supports Chrome
4. **Session Persistence:** Chrome handles persistent sessions well

---

## Troubleshooting

### Chrome Doesn't Open

**Possible causes:**
1. Chrome not installed
2. Chrome installed in non-standard location
3. Popup blocker

**Solutions:**

**1. Verify Chrome installation:**
```bash
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

**2. If Chrome is in different location:**

Edit `scripts/gmail_auth.py`, line ~125:
```python
chrome_path = 'YOUR_CHROME_PATH\\chrome.exe'
```

**3. Disable popup blocker:**
- Chrome Settings → Privacy and security → Site Settings
- Pop-ups and redirects → Allow localhost:8080

---

### WhatsApp: "Channel 'chrome' not found"

**Error:** `Error: Channel 'chrome' not found`

**Solution:** Install Google Chrome

1. Download: https://www.google.com/chrome/
2. Install
3. Run authentication again:
   ```bash
   python main.py setup-whatsapp
   ```

---

### Gmail: Browser Opens But Blank Page

**Possible causes:**
1. Popup blocker
2. Port 8080 blocked
3. Chrome profile issue

**Solution:**

**1. Try incognito mode:**
- Copy the authorization URL from terminal
- Open Chrome incognito (Ctrl+Shift+N)
- Paste URL

**2. Use different port:**
Edit `scripts/gmail_auth.py`, line ~135:
```python
creds = flow.run_local_server(port=8081, open_browser=True)
```

---

## Quick Reference

| Task | Command | Browser |
|------|---------|---------|
| **Setup Gmail** | `python main.py setup-gmail` | Chrome |
| **Setup WhatsApp** | `python main.py setup-whatsapp` | Chrome |
| **Test Gmail** | `python test_gmail_only.py` | N/A |
| **Test WhatsApp** | `python test_whatsapp_only.py` | N/A |
| **Start Gmail** | `python main.py watcher-gmail` | N/A |
| **Start WhatsApp** | `python main.py watcher-whatsapp` | Chrome (background) |

---

## Summary

✓ **Gmail authentication** - Opens Chrome automatically
✓ **WhatsApp authentication** - Opens Chrome automatically  
✓ **Fallback** - Uses default browser if Chrome not found
✓ **Error messages** - Clear instructions if Chrome missing

**Both scripts now explicitly use Google Chrome!** 🎉
