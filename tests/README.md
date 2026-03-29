# AI Employee Tests

This directory contains all test suites for the AI Employee system.

---

## 🧪 Running Tests

### Run All Tests:
```bash
# From project root
python -m tests.test_simple
python -m tests.test_ai_brain
python -m tests.test_gmail_only
python -m tests.test_whatsapp_only
```

### Or use the direct path:
```bash
python tests/test_simple.py
python tests/test_ai_brain.py
python tests/test_gmail_only.py
python tests/test_whatsapp_only.py
```

---

## 📋 Test Files

| File | Purpose | When to Run |
|------|---------|-------------|
| `test_simple.py` | Quick system check | Before running main system |
| `test_ai_brain.py` | AI Brain (Claude/Qwen) | After configuring AI |
| `test_gmail_only.py` | Gmail setup check | Before using Gmail watcher |
| `test_whatsapp_only.py` | WhatsApp setup check | Before using WhatsApp watcher |

---

## ✅ Test Descriptions

### `test_simple.py` - Quick System Check
**Purpose:** Verify all components are installed and configured

**Tests:**
- Module imports (watchers, processors)
- FileSystemWatcher functionality
- GmailWatcher structure
- WhatsAppWatcher structure
- CLI commands availability
- Documentation files

**Run when:** You want a quick health check of the system

---

### `test_ai_brain.py` - AI Brain Test Suite
**Purpose:** Test Claude and Qwen AI brain implementations

**Tests:**
- Environment configuration (.env)
- Claude processor availability
- Qwen processor availability
- AI Brain interface
- Ralph Wiggum loop
- Orchestrator integration

**Run when:** After configuring AI_BRAIN in .env

---

### `test_gmail_only.py` - Gmail Setup Check
**Purpose:** Verify Gmail integration is ready

**Tests:**
- Dependencies installed
- credentials.json exists and valid
- token.json exists (authenticated)
- GmailWatcher import works
- Gmail API connection

**Run when:** Before starting Gmail watcher

---

### `test_whatsapp_only.py` - WhatsApp Setup Check
**Purpose:** Verify WhatsApp integration is ready

**Tests:**
- Playwright installed
- Chromium browser available
- Session directory exists
- WhatsAppWatcher import works
- Session authentication status

**Run when:** Before starting WhatsApp watcher

---

## 🎯 Test Workflow

### Initial Setup:
```bash
# 1. Check everything is installed
python tests/test_simple.py

# 2. Configure AI Brain
# Edit .env file

# 3. Test AI Brain
python tests/test_ai_brain.py

# 4. Test Gmail (if using)
python tests/test_gmail_only.py

# 5. Test WhatsApp (if using)
python tests/test_whatsapp_only.py
```

### Before Running System:
```bash
# Quick health check
python tests/test_simple.py
```

### After Configuration Changes:
```bash
# Test specific component
python tests/test_ai_brain.py    # After AI config
python tests/test_gmail_only.py  # After Gmail config
python tests/test_whatsapp_only.py  # After WhatsApp config
```

---

## 📊 Interpreting Results

### All Tests Pass (✓):
```
✓ PASS: Module Imports
✓ PASS: FileSystemWatcher
✓ PASS: GmailWatcher Structure
✓ PASS: WhatsAppWatcher Structure
✓ PASS: Main CLI Commands
✓ PASS: Documentation

Total: 6/6 tests passed
```
**Meaning:** System is ready to run!

### Some Tests Fail (✗):
```
✓ PASS: Module Imports
✗ FAIL: GmailWatcher Structure
  → Error message explains what's missing
```
**Meaning:** Fix the issues listed before running the system

---

## 🔧 Troubleshooting

### Import Errors:
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution:** Run `uv sync` to install dependencies

### Path Errors:
```
FileNotFoundError: [Errno 2] No such file or directory
```
**Solution:** Run tests from project root directory

### AI Brain Not Available:
```
⚠ AI Brain not available: No module named...
```
**Solution:** Configure AI_BRAIN in .env file

---

## 📖 Additional Resources

- **Main Documentation:** `README.md`
- **AI Brain Guide:** `AI_BRAIN_GUIDE.md`
- **Quick Start:** `QUICKSTART_SILVER.md`

---

**Keep tests passing before running the main system!** ✅
