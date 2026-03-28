# Gmail and WhatsApp Testing - Complete Guide

## ✓ Dependencies Status

**All dependencies are now properly installed!**

- ✓ Google API Client: Installed
- ✓ Google OAuth2: Installed  
- ✓ Playwright: Installed
- ✓ Chromium Browser: Downloaded

---

## 📧 Gmail Watcher Testing

### File Locations

| File | Location | Purpose |
|------|----------|---------|
| **Main Script** | `main.py` | Entry point for all commands |
| **Gmail Watcher** | `watchers/gmail_watcher.py` | Monitors Gmail API |
| **Auth Script** | `scripts/gmail_auth.py` | OAuth2 authentication |
| **Test Script** | `test_gmail_only.py` | Standalone Gmail tests |
| **Credentials** | `credentials/credentials.json` | OAuth2 client config |
| **Token** | `credentials/token.json` | Access token (auto-generated) |

### Commands (Run in Order)

**1. Check Status:**
```bash
cd D:\AI_Employee
python test_gmail_only.py
```

**2. Authenticate (One-Time):**
```bash
python main.py setup-gmail
```

**What happens:**
- Browser opens automatically
- Sign in with Google account
- Grant permissions
- `token.json` created automatically

**3. Start Gmail Watcher:**
```bash
python main.py watcher-gmail
```

**Expected Output:**
```
Starting Gmail Watcher...
✓ Connected to Gmail: your-email@gmail.com
Monitoring for new emails...
```

**4. Test It:**
- Send yourself an email from another account
- Mark it as **Important** in Gmail
- Wait up to 2 minutes
- Check terminal for notification

**5. Stop Watcher:**
```bash
# Press Ctrl+C in the terminal
```

---

## 📱 WhatsApp Watcher Testing

### File Locations

| File | Location | Purpose |
|------|----------|---------|
| **Main Script** | `main.py` | Entry point for all commands |
| **WhatsApp Watcher** | `watchers/whatsapp_watcher.py` | Monitors WhatsApp Web |
| **Auth Script** | `scripts/whatsapp_init.py` | QR code authentication |
| **Test Script** | `test_whatsapp_only.py` | Standalone WhatsApp tests |
| **Session** | `sessions/whatsapp/` | Browser session data |

### Commands (Run in Order)

**1. Check Status:**
```bash
cd D:\AI_Employee
python test_whatsapp_only.py
```

**2. Authenticate (One-Time):**
```bash
python main.py setup-whatsapp
```

**What happens:**
- Browser opens with WhatsApp Web
- QR code appears on screen
- **You need to scan it with your phone**

**How to scan QR code:**
1. Open WhatsApp on your phone
2. **Android:** ⋮ → Linked devices → Link a device
3. **iPhone:** Settings → Linked Devices → Link a Device
4. Point camera at QR code on screen
5. Wait for authentication

**3. Start WhatsApp Watcher:**
```bash
python main.py watcher-whatsapp
```

**Expected Output:**
```
Starting WhatsApp Watcher...
✓ WhatsApp session is authenticated
Monitoring keywords: ['urgent', 'asap', 'invoice', 'payment', 'help']
```

**4. Test It:**
- Send yourself a WhatsApp message with keyword "urgent"
- Wait up to 30 seconds
- Check terminal for notification

**5. Stop Watcher:**
```bash
# Press Ctrl+C in the terminal
```

---

## 🚀 Quick Test Commands

### Test Everything (Automated)

```bash
# Run all tests
python test_simple.py

# Expected: 6/6 tests pass
```

### Test Gmail Only

```bash
# Run Gmail tests
python test_gmail_only.py

# Then authenticate
python main.py setup-gmail

# Then start watcher
python main.py watcher-gmail
```

### Test WhatsApp Only

```bash
# Run WhatsApp tests
python test_whatsapp_only.py

# Then authenticate
python main.py setup-whatsapp

# Then start watcher
python main.py watcher-whatsapp
```

---

## 🔧 Troubleshooting

### Gmail Issues

**Error: "ModuleNotFoundError: No module named 'google'"**

**Solution:**
```bash
uv sync
```

**Error: "Token file not found"**

**Solution:**
```bash
python main.py setup-gmail
```

**Error: "This app isn't verified"**

**Solution:**
- Click **Advanced**
- Click **Go to AI Employee (unsafe)** ← This is safe!
- Continue with authentication

**Watcher not detecting emails:**

**Check:**
- Email is **unread**
- Email is marked as **important**
- Wait up to 2 minutes (check interval)

---

### WhatsApp Issues

**Error: "ModuleNotFoundError: No module named 'playwright'"**

**Solution:**
```bash
uv sync
playwright install chromium
```

**Error: "QR Code detected"**

**Solution:**
```bash
python main.py setup-whatsapp
# Scan QR code with phone
```

**Error: "Session expired"**

**Solution:**
```bash
python main.py setup-whatsapp
# Re-authenticate
```

**Watcher not detecting messages:**

**Check:**
- Message contains keywords: `urgent`, `asap`, `invoice`, `payment`, `help`
- Wait up to 30 seconds (check interval)
- Session may have expired (re-authenticate)

---

## 📁 Complete File Structure

```
D:\AI_Employee\
│
├── main.py                          ← Main entry point (run this)
├── test_gmail_only.py               ← Test Gmail only
├── test_whatsapp_only.py            ← Test WhatsApp only
├── test_simple.py                   ← Test everything
│
├── scripts/
│   ├── gmail_auth.py                ← Gmail authentication
│   └── whatsapp_init.py             ← WhatsApp authentication
│
├── watchers/
│   ├── gmail_watcher.py             ← Gmail monitoring logic
│   └── whatsapp_watcher.py          ← WhatsApp monitoring logic
│
├── credentials/
│   ├── credentials.json             ← Download from Google Cloud
│   └── token.json                   ← Auto-generated after auth
│
├── sessions/
│   └── whatsapp/                    ← Browser session (auto-created)
│
└── AI_Employee_Vault/
    ├── Inbox/                       ← Drop files here
    ├── Needs_Action/                ← Action files created here
    └── Plans/                       ← Plans created here
```

---

## ✅ Verification Checklist

### Before Running

- [ ] Dependencies installed: `uv sync`
- [ ] Playwright browser installed: `playwright install chromium`
- [ ] Gmail credentials.json downloaded from Google Cloud
- [ ] credentials.json placed in `credentials/` folder

### After Gmail Setup

- [ ] Run: `python test_gmail_only.py`
- [ ] All tests pass
- [ ] Run: `python main.py setup-gmail`
- [ ] Browser opens and authenticates
- [ ] token.json created in `credentials/`

### After WhatsApp Setup

- [ ] Run: `python test_whatsapp_only.py`
- [ ] All tests pass
- [ ] Run: `python main.py setup-whatsapp`
- [ ] QR code appears
- [ ] Scan QR with phone
- [ ] Session saved in `sessions/whatsapp/`

### Ready to Use

- [ ] Gmail watcher: `python main.py watcher-gmail`
- [ ] WhatsApp watcher: `python main.py watcher-whatsapp`
- [ ] All watchers: `python main.py watcher-all`
- [ ] Process items: `python main.py process`

---

## 🎯 Summary

| Component | Command to Test | Command to Authenticate | Command to Run |
|-----------|----------------|------------------------|----------------|
| **Gmail** | `python test_gmail_only.py` | `python main.py setup-gmail` | `python main.py watcher-gmail` |
| **WhatsApp** | `python test_whatsapp_only.py` | `python main.py setup-whatsapp` | `python main.py watcher-whatsapp` |
| **File System** | `python test_simple.py` | None needed | `python main.py watcher` |
| **All** | `python test_simple.py` | Both above | `python main.py watcher-all` |

---

**Your AI Employee Silver Tier is fully installed and ready!** 🎉

**Next Step:** Run `python main.py setup-gmail` to authenticate Gmail.
