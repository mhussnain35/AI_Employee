# Gmail and WhatsApp Testing Guide

Complete guide for testing Gmail and WhatsApp watchers in AI Employee.

---

## Quick Test (Works Immediately)

Run the automated test suite:

```bash
python test_simple.py
```

**Expected Output:**
```
✓ PASS: Module Imports
✓ PASS: FileSystemWatcher
✓ PASS: GmailWatcher Structure
✓ PASS: WhatsAppWatcher Structure
✓ PASS: Main CLI Commands
✓ PASS: Documentation

Total: 6/6 tests passed
✓ ALL TESTS PASSED!
```

---

## Part 1: Gmail Watcher Testing

### Prerequisites

1. **Dependencies installed:**
   ```bash
   python -c "from google.oauth2.credentials import Credentials; print('OK')"
   ```

2. **Google Cloud project created** (5 minutes)
   - Go to: https://console.cloud.google.com/
   - Create new project: "AI Employee"
   - Enable Gmail API

3. **OAuth2 credentials downloaded** (3 minutes)
   - Create OAuth2 credentials (Desktop app)
   - Download `credentials.json`
   - Place in: `credentials/credentials.json`

---

### Test A: Authentication

**Command:**
```bash
python main.py setup-gmail
```

**What to expect:**

1. Browser opens automatically
2. Google sign-in page
3. "This app isn't verified" warning
   - Click **Advanced** → **Go to AI Employee (unsafe)**
4. Grant permissions
5. Success message

**Success indicators:**
```
✓ Authentication successful!
✓ Successfully connected to Gmail: your-email@gmail.com
✓ All checks passed!
```

**Verify files created:**
```bash
dir credentials\token.json
```

---

### Test B: Gmail Watcher

**1. Start watcher:**
```bash
python main.py watcher-gmail
```

**Keep terminal running!**

**Expected output:**
```
Starting Gmail Watcher...
✓ Connected to Gmail: your-email@gmail.com
Monitoring for new emails...
```

**2. Send test email:**

From another email account:
- **To:** Your Gmail address
- **Subject:** `TEST: AI Employee Test`
- **Body:** `This is a test email for the AI Employee watcher.`

**3. Mark as Important:**
- Go to Gmail
- Find the email
- Click the **Important** marker (yellow arrow)
- Keep it **unread**

**4. Wait up to 2 minutes**

**5. Check terminal:**
```
Found 1 new email(s)
Created action file: EMAIL_20260327_170000_TEST_AI_Employee_Test.md
```

**6. Verify action file:**
```bash
type AI_Employee_Vault\Needs_Action\EMAIL_*.md
```

**Expected content:**
```markdown
---
type: email
from: sender@example.com
subject: TEST: AI Employee Test
received: 2026-03-27T17:00:00
priority: high
status: pending
---

# Email: TEST: AI Employee Test

**From:** sender@example.com
**Received:** 2026-03-27 17:00:00
**Priority:** HIGH

---

## Email Content

This is a test email for the AI Employee watcher.

---

## Suggested Actions

- [ ] Read and understand the email
- [ ] Determine if reply is needed
- [ ] Move to /Done when complete
```

**✓ Gmail Test PASSED!**

**Stop watcher:** Press `Ctrl+C`

---

## Part 2: WhatsApp Watcher Testing

### Prerequisites

1. **Playwright installed:**
   ```bash
   python -c "from playwright.sync_api import sync_playwright; print('OK')"
   ```

2. **Chromium browser installed:**
   ```bash
   playwright install chromium
   ```

---

### Test A: Authentication

**Command:**
```bash
python main.py setup-whatsapp
```

**What to expect:**

1. Browser window opens (visible)
2. Navigates to WhatsApp Web
3. QR code appears on screen

**Terminal shows:**
```
============================================================
WhatsApp Web Authentication
============================================================

Steps to authenticate:
1. Wait for QR code to appear
2. Open WhatsApp on your phone
3. Go to Settings → Linked Devices
4. Tap 'Link a Device'
5. Scan the QR code

Monitoring for authentication...
```

**Scan QR code with phone:**

**Android:**
1. WhatsApp → ⋮ → Linked devices
2. Link a device
3. Scan QR code

**iPhone:**
1. WhatsApp → Settings → Linked Devices
2. Link a Device
3. Scan QR code

**Success indicators:**
```
✓ Authentication successful!
✓ Session is valid and authenticated

WhatsApp Authentication Complete!
Session saved to: sessions\whatsapp
```

**Verify session saved:**
```bash
dir sessions\whatsapp
```

---

### Test B: WhatsApp Watcher

**1. Start watcher:**
```bash
python main.py watcher-whatsapp
```

**Keep terminal running!**

**Expected output:**
```
Starting WhatsApp Watcher...
✓ WhatsApp session is authenticated
Monitoring keywords: ['urgent', 'asap', 'invoice', 'payment', 'help']
Check interval: 30s
Monitoring for urgent messages...
```

**2. Send test WhatsApp message:**

From your phone (or ask a friend):

Send a message containing one of these keywords:
- `urgent`
- `asap`
- `invoice`
- `payment`
- `help`

**Example message:**
```
urgent: Please call me back ASAP!
```

**3. Wait up to 30 seconds**

**4. Check terminal:**
```
Found 1 urgent message(s)
Created action file: WHATSAPP_20260327_170500_+1234567890.md
```

**5. Verify action file:**
```bash
type AI_Employee_Vault\Needs_Action\WHATSAPP_*.md
```

**Expected content:**
```markdown
---
type: whatsapp
from: +1234567890
received: 2026-03-27T17:05:00
priority: high
status: pending
keywords_detected: ['urgent', 'asap']
---

# WhatsApp Message

**From:** +1234567890
**Received:** 2026-03-27 17:05:00
**Priority:** HIGH

---

## Message Content

urgent: Please call me back ASAP!

---

## Suggested Actions

- [ ] Read and understand the message
- [ ] Determine if reply is needed
- [ ] Move to /Done when complete
```

**✓ WhatsApp Test PASSED!**

**Stop watcher:** Press `Ctrl+C`

---

## Part 3: Test All Watchers Together

**Start all watchers:**
```bash
python main.py watcher-all
```

**Expected output:**
```
Starting All Watchers...

Starting File System Watcher...
Starting Gmail Watcher...
Starting WhatsApp Watcher...

✓ All watchers started
Monitoring for new items...
```

**Test all three:**

1. **File:** Drop a file in `AI_Employee_Vault/Inbox/test.txt`
2. **Email:** Send yourself a Gmail (mark important)
3. **WhatsApp:** Send a message with "urgent"

**Watch terminal:**
```
FileSystemWatcher - New file detected: test.txt
GmailWatcher - Found 1 new email(s)
WhatsAppWatcher - Found 1 urgent message(s)
```

**Stop watchers:** Press `Ctrl+C`

---

## Part 4: Process All Items

After watchers create action files:

```bash
python main.py process
```

**Expected output:**
```
============================================================
AI Employee Orchestrator
============================================================
Found 3 pending item(s)

Processing: FILE_20260327_170000_test.txt.md
✓ Created plan: PLAN_*.md

Processing: EMAIL_20260327_170000_TEST.md
✓ Created plan: PLAN_*.md

Processing: WHATSAPP_20260327_170000_+1234567890.md
✓ Created plan: PLAN_*.md

Processing Complete: 3/3 items
============================================================
```

**Verify plans created:**
```bash
dir AI_Employee_Vault\Plans\
```

---

## Troubleshooting

### Gmail Tests Fail

**Problem:** "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
uv sync
```

**Problem:** "credentials.json not found"

**Solution:**
1. Download from Google Cloud Console
2. Place in `credentials/credentials.json`

**Problem:** "Token refresh failed"

**Solution:**
```bash
del credentials\token.json
python main.py setup-gmail
```

**Problem:** Gmail watcher not detecting emails

**Check:**
- Email is **unread**
- Email is marked as **important**
- Wait up to 2 minutes (check interval)

---

### WhatsApp Tests Fail

**Problem:** "ModuleNotFoundError: No module named 'playwright'"

**Solution:**
```bash
uv sync
playwright install chromium
```

**Problem:** "QR Code detected - Authentication required"

**Solution:**
```bash
python main.py setup-whatsapp
```

**Problem:** WhatsApp watcher not detecting messages

**Check:**
- Message contains keywords: urgent, asap, invoice, payment, help
- Wait up to 30 seconds (check interval)
- Session may have expired (re-run setup-whatsapp)

---

## Test Results Summary

| Test | Command | Works Without Setup? |
|------|---------|---------------------|
| **Module Imports** | `python test_simple.py` | ✓ Yes |
| **FileSystemWatcher** | `python main.py watcher` | ✓ Yes |
| **Gmail Structure** | `python test_simple.py` | ✓ Yes |
| **Gmail Auth** | `python main.py setup-gmail` | ✗ Need credentials.json |
| **Gmail Watcher** | `python main.py watcher-gmail` | ✗ Need authentication |
| **WhatsApp Structure** | `python test_simple.py` | ✓ Yes |
| **WhatsApp Auth** | `python main.py setup-whatsapp` | ✓ Yes (shows QR) |
| **WhatsApp Watcher** | `python main.py watcher-whatsapp` | ✗ Need session |
| **All Watchers** | `python main.py watcher-all` | Partial (File only) |

---

## Quick Reference

### Commands

```bash
# Test everything
python test_simple.py

# Setup
python main.py setup-gmail         # Gmail authentication
python main.py setup-whatsapp      # WhatsApp authentication

# Run watchers
python main.py watcher             # File system only
python main.py watcher-gmail       # Gmail only
python main.py watcher-whatsapp    # WhatsApp only
python main.py watcher-all         # All watchers

# Process items
python main.py process
```

### File Locations

```
credentials/
├── credentials.json    # Gmail OAuth2 (download from Google)
└── token.json          # Auto-generated by setup-gmail

sessions/
└── whatsapp/           # Browser session (auto-generated)

AI_Employee_Vault/
├── Inbox/              # Drop files here
├── Needs_Action/       # Action files created here
├── Plans/              # Plans created by orchestrator
└── Done/               # Completed items
```

---

## Next Steps After Testing

1. ✓ Run `python test_simple.py` - All tests pass
2. ✓ Run `python main.py setup-gmail` - Gmail authenticated
3. ✓ Run `python main.py setup-whatsapp` - WhatsApp authenticated
4. ✓ Run `python main.py watcher-all` - All watchers running
5. ✓ Send test email and WhatsApp message
6. ✓ Run `python main.py process` - Items processed

**Your AI Employee is now fully operational!** 🎉

---

*For detailed setup instructions, see:*
- `docs/GMAIL_SETUP.md` - Gmail setup guide
- `docs/WHATSAPP_SETUP.md` - WhatsApp setup guide
- `QUICKSTART_SILVER.md` - Quick start guide
