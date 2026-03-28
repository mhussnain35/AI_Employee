# AI Employee - Your Personal Digital FTE

**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

A **Digital FTE (Full-Time Equivalent)** is an AI agent that works for you 24/7, proactively managing your personal and business affairs using **Claude Code** as the reasoning engine and **Obsidian** as the management dashboard.

---

## Quick Start

### Prerequisites
- Python 3.11+
- UV package manager
- Obsidian (optional, for viewing vault)
- Claude Code subscription (optional, for AI processing)

### Installation

```bash
# Clone or navigate to the project
cd AI_Employee

# Install dependencies (using UV)
uv sync

# Install Playwright browsers
playwright install chromium
```

### Usage

```bash
# Show status and help
python main.py

# Setup authentication (Silver Tier)
python main.py setup-gmail
python main.py setup-whatsapp

# Start watchers
python main.py watcher          # File system only
python main.py watcher-gmail    # Gmail only
python main.py watcher-whatsapp # WhatsApp only
python main.py watcher-all      # All watchers in parallel

# Process pending items
python main.py process
```

---

## Current Tier: Silver ✓

The Silver Tier includes **all Bronze features** plus:

### ✓ Gmail Integration
- OAuth2 authentication with auto-refresh
- Monitors unread and important emails
- Creates action files with full email content
- Priority detection from headers
- Token auto-refresh mechanism

### ✓ WhatsApp Integration
- Playwright with Chromium browser
- Persistent session (scan QR code once)
- Keyword monitoring (urgent, asap, invoice, payment, help)
- Auto-reconnect on session expiry
- Real-time message detection

### ✓ Security & Configuration
- `.env.example` - Environment variables template
- Secure credential storage (`credentials/`, `sessions/`)
- Comprehensive security documentation
- Step-by-step setup guides

### ✓ Enhanced CLI
- `setup-gmail` - OAuth2 authentication
- `setup-whatsapp` - QR code scanning
- `watcher-gmail` - Gmail watcher only
- `watcher-whatsapp` - WhatsApp watcher only
- `watcher-all` - All watchers in parallel

### Complete Folder Structure

```
AI_Employee/
├── main.py                         # Main CLI with all commands
├── orchestrator.py                 # Processes pending items
├── setup_vault.py                  # Initializes vault structure
├── .env.example                    # Environment variables template
├── SECURITY.md                     # Security documentation
├── QUICKSTART_SILVER.md            # Quick start guide
│
├── scripts/
│   ├── gmail_auth.py              # Gmail OAuth2 setup
│   └── whatsapp_init.py           # WhatsApp QR code scanner
│
├── watchers/
│   ├── base_watcher.py            # Abstract base class
│   ├── filesystem_watcher.py      # File monitoring (Bronze)
│   ├── gmail_watcher.py           # Gmail API (Silver)
│   └── whatsapp_watcher.py        # WhatsApp Web (Silver)
│
├── docs/
│   ├── GMAIL_SETUP.md             # Gmail setup guide
│   └── WHATSAPP_SETUP.md          # WhatsApp setup guide
│
├── credentials/
│   ├── credentials.json           # From Google Cloud (git-ignored)
│   └── token.json                 # Auto-generated (git-ignored)
│
├── sessions/
│   └── whatsapp/                  # Browser session (git-ignored)
│
├── AI_Employee_Vault/
│   ├── Dashboard.md               # Real-time stats dashboard
│   ├── Company_Handbook.md        # Rules of engagement
│   ├── README.md                  # Vault documentation
│   ├── Inbox/                     # Drop folder for new files
│   ├── Needs_Action/              # Items requiring attention
│   ├── Done/                      # Completed tasks
│   ├── Plans/                     # Action plans
│   └── Pending_Approval/          # Awaiting human approval
│
└── Tests/
    ├── test_watcher.py            # Bronze Tier tests
    ├── test_e2e.py                # Bronze Tier E2E
    ├── test_gmail_watcher.py      # Gmail tests
    ├── test_whatsapp_watcher.py   # WhatsApp tests
    └── test_silver_e2e.py         # Silver Tier E2E
```

---

## How It Works

### Architecture: Perception → Reasoning → Action

#### 1. Perception (Watchers)

Lightweight Python scripts run continuously, monitoring various inputs:

- **FileSystemWatcher** (Bronze): Monitors `Inbox/` folder for new files (every 5s)
- **GmailWatcher** (Silver): Monitors Gmail for new emails (every 2m)
  - Uses Gmail API with OAuth2 authentication
  - Filters unread and important messages
  - Auto-refreshes tokens
- **WhatsAppWatcher** (Silver): Monitors WhatsApp Web for urgent messages (every 30s)
  - Uses Playwright with Chromium
  - Persistent browser session
  - Keyword detection (urgent, asap, invoice, payment, help)

When a watcher detects a new item, it creates an action file in `Needs_Action/`.

#### 2. Reasoning (Claude Code)
The orchestrator processes items in `Needs_Action/`:

1. Reads the action file content
2. Consults `Company_Handbook.md` for rules
3. Creates a plan in `Plans/` with checkboxes
4. Executes actions or requests approval

#### 3. Action (Hands)

Claude Code uses MCP (Model Context Protocol) servers to act:

- **Filesystem MCP**: Read/write files in the vault (Built-in)
- **Email MCP** (Gold): Send emails via Gmail API
- **Browser MCP** (Gold): Web automation for payments
- **WhatsApp MCP** (Future): Send WhatsApp messages
- **Calendar MCP** (Gold): Schedule meetings
- **Social Media MCP** (Gold): Post to LinkedIn, Twitter, etc.

#### 4. Human-in-the-Loop
For sensitive actions:

1. Claude creates file in `Pending_Approval/`
2. Human reviews and moves to `Approved/` or `Rejected/`
3. Claude executes approved actions

---

## Workflow Example

### Step 1: Drop a File
Place any file in `AI_Employee_Vault/Inbox/`:
```
client_invoice_request.txt
```

### Step 2: Watcher Detects
The FileSystemWatcher automatically creates an action file:
```
Needs_Action/FILE_20260327_153650_client_invoice_request.txt.md
```

### Step 3: Process Item
Run the orchestrator:
```bash
python main.py process
```

### Step 4: Plan Created
A plan is created in `Plans/`:
```markdown
# Action Plan: client_invoice_request.txt

## Required Actions
- [ ] Review the invoice request
- [ ] Check Company Handbook rules (amount > $500 requires approval)
- [ ] Create invoice draft
- [ ] Move to Pending_Approval if amount > $500
```

### Step 5: Human Approval (if needed)
For amounts > $500, Claude moves the file to `Pending_Approval/` for your review.

---

## Configuration

### Claude Code Setup

1. Copy `claude_config.json` to your Claude Code config directory:
   - Windows: `%APPDATA%\claude-code\mcp.json`
   - Mac/Linux: `~/.config/claude-code/mcp.json`

2. Update the vault path in the configuration

3. Start Claude Code:
   ```bash
   claude
   ```

4. Prompt Claude to process your vault:
   ```
   Check the Needs_Action folder and process all pending items
   according to the Company Handbook rules.
   ```

---

## Company Handbook Rules

The `Company_Handbook.md` contains your rules of engagement:

### Communication Rules
- Always be polite and professional
- Respond to urgent messages within 1 hour
- Flag VIP contacts for immediate attention

### Financial Rules
| Amount | Action Required |
|--------|-----------------|
| < $100 | Auto-log only |
| $100 - $500 | Log + notify human |
| > $500 | Require approval before action |

### Task Priority Levels
1. **Critical**: Response within 1 hour
2. **High**: Response within 4 hours
3. **Normal**: Response within 24 hours
4. **Low**: Response within 1 week

---

## Testing

### Run Unit Tests
```bash
# Test the FileSystemWatcher
python test_watcher.py

# Run end-to-end test
python test_e2e.py
```

### Expected Output
All tests should pass with:
- ✓ Action files created in Needs_Action
- ✓ Plans generated in Plans folder
- ✓ Dashboard updated with stats

---

## Dependencies

Current dependencies (managed by UV):

- `watchdog>=6.0.0` - File system monitoring

To add new dependencies:
```bash
uv add <package-name>
```

**Important:** Always use `uv add`, not `pip install`.

---

## Next Steps (Silver Tier)

To upgrade to **Silver Tier**, implement:

1. **Gmail Watcher**: Monitor Gmail API for new emails
2. **WhatsApp Watcher**: Use Playwright for WhatsApp Web automation
3. **MCP Server**: Implement email-sending capability
4. **Scheduling**: Add cron/Task Scheduler integration
5. **LinkedIn Integration**: Auto-post business updates

---

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Main entry point with CLI commands |
| `orchestrator.py` | Processes pending items with Claude Code |
| `setup_vault.py` | Initializes vault folder structure |
| `watchers/base_watcher.py` | Abstract base class for all watchers |
| `watchers/filesystem_watcher.py` | Monitors Inbox folder |
| `test_watcher.py` | Unit tests for watcher |
| `test_e2e.py` | End-to-end integration tests |
| `claude_config.json` | Claude Code MCP configuration template |

---

## License & Credits

This project is part of the **Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026**.

**Resources:**
- [Requirements Document](reqment.md)
- [Claude Code Documentation](https://claude.com/product/claude-code)
- [Obsidian Documentation](https://obsidian.md)
- [MCP Servers](https://github.com/modelcontextprotocol)

**Weekly Meetings:** Wednesdays at 10:00 PM PKT on Zoom
- Meeting ID: 871 8870 7642
- Passcode: 744832

---

*Your AI Employee works 168 hours/week vs a human's 40 hours. That's 4.2x more availability at ~10% of the cost.*
