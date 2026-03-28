# Quick Authentication Guide

## ✓ Authentication Issues Fixed!

The test scripts no longer prompt for authentication. They now only **check status** and tell you what to do next.

---

## 📧 Gmail Authentication

### Step 1: Test First

```bash
python test_gmail_only.py
```

**Expected output if not authenticated:**
```
✗ FAIL: Authentication Status
  → Run: python main.py setup-gmail
```

### Step 2: Authenticate

```bash
python main.py setup-gmail
```

**What happens:**

1. **Browser opens automatically**
2. **Google sign-in page appears**
3. **Sign in** with your Google account
4. **Warning screen appears:** "This app isn't verified"
   - Click **"Advanced"**
   - Click **"Go to AI Employee (unsafe)"** ← **This is safe!**
   - This warning appears because it's a personal app (not for public use)
5. **Click "Allow"** to grant Gmail read permissions
6. **Browser shows:** "Authentication complete"
7. **Terminal shows:**
   ```
   ✓ Authentication successful!
   ✓ Token saved successfully
   Next step: python main.py watcher-gmail
   ```

### Step 3: Verify

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

## 📱 WhatsApp Authentication

### Step 1: Test First

```bash
python test_whatsapp_only.py
```

**Expected output if not authenticated:**
```
✗ FAIL: Session Status
  → Run: python main.py setup-whatsapp
```

### Step 2: Authenticate

```bash
python main.py setup-whatsapp
```

**What happens:**

1. **Browser window opens** (visible, not hidden)
2. **Navigates to WhatsApp Web**
3. **QR code appears on screen**

**Terminal shows:**
```
Please scan the QR code with your WhatsApp mobile app
Monitoring for authentication (2 minutes max)...
```

### Step 3: Scan QR Code

**On Android:**
1. Open **WhatsApp** app
2. Tap **⋮** (three dots menu)
3. Tap **"Linked devices"**
4. Tap **"Link a device"**
5. **Point camera at QR code** on computer screen

**On iPhone:**
1. Open **WhatsApp** app
2. Go to **Settings** (gear icon)
3. Tap **"Linked Devices"**
4. Tap **"Link a Device"**
5. **Point camera at QR code** on computer screen

**What happens next:**
- Phone vibrates when QR code scans successfully
- Browser shows your WhatsApp chats loading
- Terminal shows:
  ```
  ✓ Authentication successful!
  Session will be saved automatically.
  ```

### Step 4: Verify

```bash
python test_whatsapp_only.py
```

**Expected output:**
```
✓ PASS: Session Status
✓ WhatsApp is ready!
  → Run: python main.py watcher-whatsapp
```

---

## 🚀 Start Using

### Start Gmail Watcher

```bash
python main.py watcher-gmail
```

**Expected:**
```
Starting Gmail Watcher...
✓ Connected to Gmail: your-email@gmail.com
Monitoring for new emails...
```

**Test it:**
1. Send yourself an email from another account
2. Mark it as **Important** in Gmail
3. Wait up to 2 minutes
4. Check terminal for notification

---

### Start WhatsApp Watcher

```bash
python main.py watcher-whatsapp
```

**Expected:**
```
Starting WhatsApp Watcher...
✓ WhatsApp session is authenticated
Monitoring keywords: ['urgent', 'asap', 'invoice', 'payment', 'help']
```

**Test it:**
1. Send yourself a WhatsApp message with word "urgent"
2. Wait up to 30 seconds
3. Check terminal for notification

---

### Start All Watchers

```bash
python main.py watcher-all
```

This runs all 3 watchers in parallel:
- File System Watcher (checks every 5s)
- Gmail Watcher (checks every 120s)
- WhatsApp Watcher (checks every 30s)

---

## ⚠️ Troubleshooting

### Gmail: "This app isn't verified"

**This is normal and expected!**

**Why:** Google shows this for apps that haven't gone through their verification process (personal apps).

**Solution:**
1. Click **"Advanced"**
2. Click **"Go to AI Employee (unsafe)"**
3. Continue with authentication

**This is safe** because:
- It's your own app
- You created the credentials
- It only requests read-only Gmail access

---

### Gmail: Port 8080 blocked

**Error:** "Port 8080 is blocked"

**Solution 1:** Run as administrator
```bash
# Windows: Right-click Command Prompt → Run as Administrator
python main.py setup-gmail
```

**Solution 2:** Use different port
Edit `scripts/gmail_auth.py`, change:
```python
creds = flow.run_local_server(port=8081, open_browser=True)
```

---

### WhatsApp: QR code doesn't appear

**Possible causes:**
1. Network connection issue
2. WhatsApp Web down
3. Browser blocked by firewall

**Solution:**
1. Check internet connection
2. Try opening [web.whatsapp.com](https://web.whatsapp.com) manually
3. Disable firewall temporarily
4. Re-run: `python main.py setup-whatsapp`

---

### WhatsApp: Authentication timeout

**Error:** "Authentication timeout after 2 minutes"

**Possible reasons:**
1. QR code expired (they refresh every ~60 seconds)
2. QR code was not scanned in time
3. Network issue

**Solution:**
```bash
python main.py setup-whatsapp
# Try again, scan QR code faster
```

---

### WhatsApp: Session expired

**Error:** "Session may be expired"

**Solution:**
```bash
python main.py setup-whatsapp
# Re-authenticate
```

**Session lifetime:** Typically lasts several days to weeks.

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| **Test Gmail** | `python test_gmail_only.py` |
| **Authenticate Gmail** | `python main.py setup-gmail` |
| **Start Gmail** | `python main.py watcher-gmail` |
| **Test WhatsApp** | `python test_whatsapp_only.py` |
| **Authenticate WhatsApp** | `python main.py setup-whatsapp` |
| **Start WhatsApp** | `python main.py watcher-whatsapp` |
| **Start All** | `python main.py watcher-all` |

---

## ✅ Checklist

### Before Authentication
- [ ] Dependencies installed: `uv sync`
- [ ] Playwright browser: `playwright install chromium`
- [ ] Gmail credentials.json downloaded

### After Gmail Authentication
- [ ] `python test_gmail_only.py` passes
- [ ] `credentials/token.json` exists
- [ ] Can run `python main.py watcher-gmail`

### After WhatsApp Authentication
- [ ] `python test_whatsapp_only.py` passes
- [ ] `sessions/whatsapp/` folder has data
- [ ] Can run `python main.py watcher-whatsapp`

---

**Your AI Employee is ready!** 🎉

For detailed guides, see:
- `docs/GMAIL_SETUP.md` - Detailed Gmail setup
- `docs/WHATSAPP_SETUP.md` - Detailed WhatsApp setup
- `TESTING_GUIDE.md` - Complete testing guide
