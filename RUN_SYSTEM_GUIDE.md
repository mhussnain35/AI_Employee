# AI Employee System Runner - Quick Guide

## ✓ Complete System Started Successfully!

---

## 🚀 How to Run

### **Option 1: Using run_system.py (RECOMMENDED)**

```bash
python run_system.py
```

This is the **main entry point** that starts everything automatically.

---

### **Option 2: Using main.py**

```bash
python main.py run
```

Same as above, just a different command.

---

## 📋 What It Does

When you run `python run_system.py`, it:

### **Step 1: Checks Obsidian Vault**
- ✓ Verifies all folders exist
- ✓ Checks key files (Dashboard.md, Company_Handbook.md)
- ✓ Creates missing components automatically

### **Step 2: Checks Gmail Authentication**
- ✓ Verifies credentials.json exists
- ✓ Checks token.json is valid
- ✓ Auto-refreshes expired tokens
- ⚠ Skips Gmail watcher if not authenticated

### **Step 3: Checks WhatsApp Authentication**
- ✓ Tests existing session
- ✓ Verifies browser can connect
- ⚠ Skips WhatsApp watcher if not authenticated

### **Step 4: Starts Watchers**
- ✓ **File System Watcher** (checks every 5s)
- ✓ **Gmail Watcher** (if authenticated, checks every 2m)
- ✓ **WhatsApp Watcher** (if authenticated, checks every 30s)

### **Step 5: Starts Orchestrator**
- ✓ Processes any pending items in Needs_Action/
- ✓ Creates plans for each item
- ✓ Follows Company Handbook rules

---

## 🎯 Expected Output

```
╔══════════════════════════════════════════════════════════╗
║           AI Employee - Your Digital FTE                 ║
╚══════════════════════════════════════════════════════════╝

======================================================================
Step 1: Checking Obsidian Vault
======================================================================
  ✓ Inbox/
  ✓ Needs_Action/
  ✓ Done/
  ✓ Plans/
  ✓ Pending_Approval/
  ✓ Dashboard.md
  ✓ Company_Handbook.md

  ✓ Obsidian Vault is ready!

======================================================================
Step 2: Checking Gmail Authentication
======================================================================
  ✓ Gmail is authenticated!

======================================================================
Step 3: Checking WhatsApp Authentication
======================================================================
  ✓ WhatsApp session is active!

======================================================================
Step 4: Starting Watchers
======================================================================
  ✓ File System Watcher started (checking every 5s)
  ✓ Gmail Watcher started (checking every 2m)
  ✓ WhatsApp Watcher started (checking every 30s)

======================================================================
Step 5: Starting Orchestrator
======================================================================
  ✓ No pending items to process

======================================================================
System Status
======================================================================
  Active Watchers:
    ✓ File System Watcher
    ✓ Gmail Watcher
    ✓ WhatsApp Watcher

  Items:
    • Needs Action: 0
    • Plans: 0
    • Done: 0

======================================================================
✓ AI Employee System is RUNNING!
======================================================================

  Monitoring for new items...
  Press Ctrl+C to stop
```

---

## 🛑 How to Stop

Press **`Ctrl+C`** in the terminal.

The system will:
- Stop all watchers gracefully
- Save any pending changes
- Exit cleanly

---

## 📊 What Runs in the Background

### **File System Watcher**
- Monitors: `AI_Employee_Vault/Inbox/`
- Check interval: Every 5 seconds
- Creates: Action files in `Needs_Action/`

### **Gmail Watcher** (if authenticated)
- Monitors: Gmail API for new emails
- Check interval: Every 2 minutes
- Filters: Unread & Important emails
- Creates: Email action files in `Needs_Action/`

### **WhatsApp Watcher** (if authenticated)
- Monitors: WhatsApp Web for messages
- Check interval: Every 30 seconds
- Filters: Messages with keywords (urgent, asap, invoice, payment, help)
- Creates: WhatsApp action files in `Needs_Action/`

### **Orchestrator**
- Processes: All items in `Needs_Action/`
- Creates: Plans in `Plans/` folder
- Follows: Company Handbook rules

---

## ⚙️ Authentication Status

### **Gmail**

**If authenticated:**
```
✓ Gmail Watcher started (checking every 2m)
```

**If not authenticated:**
```
⊘ Gmail Watcher: Skipped (not authenticated)
   Run 'python main.py setup-gmail' to enable
```

**To authenticate:**
```bash
python main.py setup-gmail
```

---

### **WhatsApp**

**If authenticated:**
```
✓ WhatsApp Watcher started (checking every 30s)
```

**If not authenticated:**
```
⊘ WhatsApp Watcher: Skipped (not authenticated)
   Run 'python main.py setup-whatsapp' to enable
```

**To authenticate:**
```bash
python main.py setup-whatsapp
```

---

## 🧪 Testing the System

### **1. Test File Watcher**

While system is running:

```bash
# Create a test file
echo "Test message" > AI_Employee_Vault/Inbox/test.txt

# Wait 5-10 seconds

# Check Needs_Action folder
dir AI_Employee_Vault\Needs_Action\

# You should see: FILE_*_test.txt.md
```

---

### **2. Test Gmail** (if authenticated)

1. Send yourself an email
2. Mark it as **Important**
3. Wait up to 2 minutes
4. Check terminal for notification
5. Check `AI_Employee_Vault/Needs_Action/` folder

---

### **3. Test WhatsApp** (if authenticated)

1. Send yourself a WhatsApp message with "urgent"
2. Wait up to 30 seconds
3. Check terminal for notification
4. Check `AI_Employee_Vault/Needs_Action/` folder

---

## 📁 File Structure

```
AI_Employee/
├── run_system.py              ← Main system runner (USE THIS)
├── main.py                    ← Also works: python main.py run
│
├── watchers/
│   ├── filesystem_watcher.py  ← Monitors Inbox folder
│   ├── gmail_watcher.py       ← Monitors Gmail API
│   └── whatsapp_watcher.py    ← Monitors WhatsApp Web
│
├── orchestrator.py            ← Processes action items
│
├── AI_Employee_Vault/
│   ├── Inbox/                 ← Drop files here
│   ├── Needs_Action/          ← Action files created here
│   ├── Plans/                 ← Plans created here
│   ├── Done/                  ← Completed items
│   ├── Dashboard.md           ← System dashboard
│   └── Company_Handbook.md    ← Rules & guidelines
│
├── credentials/
│   ├── credentials.json       ← Gmail OAuth2 credentials
│   └── token.json             ← Gmail access token
│
└── sessions/
    └── whatsapp/              ← WhatsApp browser session
```

---

## 🔧 Troubleshooting

### **System Won't Start**

**Error:** "Module not found"

**Solution:**
```bash
uv sync
python run_system.py
```

---

### **Gmail Not Starting**

**Message:** "Gmail Watcher: Skipped (not authenticated)"

**Solution:**
```bash
python main.py setup-gmail
# Then restart system
python run_system.py
```

---

### **WhatsApp Not Starting**

**Message:** "WhatsApp Watcher: Skipped (not authenticated)"

**Solution:**
```bash
python main.py setup-whatsapp
# Then restart system
python run_system.py
```

---

### **Orchestrator Not Processing**

**Issue:** Items in Needs_Action/ not being processed

**Solution:**
```bash
# Check orchestrator manually
python main.py process

# Then restart system
python run_system.py
```

---

## 📖 Quick Reference

| Task | Command |
|------|---------|
| **Start System** | `python run_system.py` |
| **Start System (alt)** | `python main.py run` |
| **Stop System** | Press `Ctrl+C` |
| **Setup Gmail** | `python main.py setup-gmail` |
| **Setup WhatsApp** | `python main.py setup-whatsapp` |
| **Check Status** | `python main.py status` |
| **Test All** | `python test_simple.py` |

---

## ✅ Checklist

Before running:
- [ ] Dependencies installed: `uv sync`
- [ ] Vault exists (auto-created if missing)
- [ ] Gmail authenticated (optional but recommended)
- [ ] WhatsApp authenticated (optional but recommended)

After running:
- [ ] All watchers started
- [ ] Orchestrator processed pending items
- [ ] System monitoring for new items
- [ ] Can stop with Ctrl+C

---

## 🎯 Summary

**`python run_system.py`** is your **one command** to start the complete AI Employee system.

It automatically:
1. ✓ Checks everything is ready
2. ✓ Starts all available watchers
3. ✓ Processes pending items
4. ✓ Monitors for new activity
5. ✓ Runs until you stop it (Ctrl+C)

**No configuration needed - just run it!**

---

**Your AI Employee is now running 24/7!** 🎉
