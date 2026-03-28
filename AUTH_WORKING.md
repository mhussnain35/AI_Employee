# Authentication is Working! ✓

## Current Status

The `python main.py setup-gmail` command is now **working correctly**!

The browser opened and displayed:
```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?...
```

---

## What to Do Now

### 1. Complete Gmail Authentication

**The browser window should be open.** If not, click the URL in the terminal output.

**Steps:**
1. **Sign in** with your Google account
2. **You'll see:** "This app isn't verified"
   - Click **"Advanced"**
   - Click **"Go to AI Employee (unsafe)"** ← **This is safe!**
3. **Click "Allow"** to grant Gmail read permissions
4. **Browser will show:** "Authentication complete"
5. **Terminal will show:**
   ```
   ✓ Authentication successful!
   ✓ Token saved successfully
   Next step: python main.py watcher-gmail
   ```

---

### 2. Verify Gmail Setup

After authentication completes:

```bash
python test_gmail_only.py
```

**Expected output:**
```
✓ PASS: Authentication Status
✓ Gmail is authenticated and ready!
  → Run: python main.py watcher-gmail
```

---

### 3. Start Gmail Watcher

```bash
python main.py watcher-gmail
```

**Expected output:**
```
Starting Gmail Watcher...
✓ Connected to Gmail: your-email@gmail.com
Monitoring for new emails...
```

---

## If Browser Didn't Open

### Manual Authorization

1. **Copy the URL** from the terminal output
2. **Paste in browser** (Chrome, Edge, Firefox)
3. **Follow steps above** to authorize

### If Port 8080 is Blocked

**Error:** "Port 8080 is already in use"

**Solution:** Run as Administrator
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Run: `python main.py setup-gmail`

---

## WhatsApp Authentication

After Gmail is done, authenticate WhatsApp:

```bash
python main.py setup-whatsapp
```

**What happens:**
1. Browser opens with WhatsApp Web
2. QR code appears
3. Scan with your phone:
   - **Android:** WhatsApp → ⋮ → Linked devices → Link a device
   - **iPhone:** WhatsApp → Settings → Linked Devices → Link a Device
4. Session saved automatically

---

## Quick Reference

| Task | Command | Status |
|------|---------|--------|
| **Test Gmail** | `python test_gmail_only.py` | ✓ Working |
| **Authenticate Gmail** | `python main.py setup-gmail` | ✓ Working (browser open) |
| **Start Gmail** | `python main.py watcher-gmail` | Ready after auth |
| **Test WhatsApp** | `python test_whatsapp_only.py` | ✓ Working |
| **Authenticate WhatsApp** | `python main.py setup-whatsapp` | Ready to use |
| **Start WhatsApp** | `python main.py watcher-whatsapp` | Ready after auth |
| **Start All** | `python main.py watcher-all` | Ready after both auth |

---

## Troubleshooting

### Error: "Module not found"

**If you see:** `ModuleNotFoundError: No module named 'google_auth_oauthlib'`

**Solution:**
```bash
# Clear Python cache
rmdir /s /q scripts\__pycache__ 2>nul
rmdir /s /q watchers\__pycache__ 2>nul
rmdir /s /q __pycache__ 2>nul

# Re-sync dependencies
uv sync

# Try again
python main.py setup-gmail
```

### Error: "Port 8080 is blocked"

**Solution:** Use different port

Edit `scripts/gmail_auth.py`, line ~120:
```python
creds = flow.run_local_server(port=8081, open_browser=True)
```

Then run again:
```bash
python main.py setup-gmail
```

### Browser Shows Blank Page

**Possible causes:**
1. Popup blocker prevented redirect
2. Network issue
3. Browser compatibility

**Solution:**
1. Disable popup blocker for localhost
2. Try a different browser (Chrome, Edge, Firefox)
3. Copy/paste the authorization URL manually

---

## Next Steps After Authentication

1. ✓ Complete Gmail authentication (browser is open now)
2. ✓ Verify: `python test_gmail_only.py`
3. ✓ Authenticate WhatsApp: `python main.py setup-whatsapp`
4. ✓ Verify: `python test_whatsapp_only.py`
5. ✓ Start all watchers: `python main.py watcher-all`

---

**Your authentication is working! Just complete the authorization in the browser.** 🎉

For detailed guides:
- `QUICK_AUTH.md` - Quick authentication guide
- `docs/GMAIL_SETUP.md` - Detailed Gmail setup
- `docs/WHATSAPP_SETUP.md` - Detailed WhatsApp setup
