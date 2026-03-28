# AI Employee Vault

This is your Personal AI Employee's Obsidian vault. It serves as the **Brain** and **Memory** for your AI Employee.

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md          # Main dashboard with real-time stats
├── Company_Handbook.md   # Rules of engagement and guidelines
├── Inbox/                # Drop folder for new files/messages
├── Needs_Action/         # Items requiring immediate attention
├── Done/                 # Completed tasks
├── Plans/                # Action plans created by Claude
├── Pending_Approval/     # Actions waiting for human approval
├── Briefings/            # CEO briefings and reports
└── Updates/              # System updates and logs
```

## How It Works

### 1. Watcher Scripts
Lightweight Python scripts monitor:
- **File System**: Watches the `Inbox/` folder for new files
- **Gmail**: (Future) Monitors for new emails
- **WhatsApp**: (Future) Monitors for urgent messages

### 2. Claude Code Processing
When items appear in `Needs_Action/`:
1. Run: `python orchestrator.py`
2. Claude Code reads the item and Company Handbook
3. Creates a plan in `Plans/`
4. Executes actions or requests approval

### 3. Human-in-the-Loop
For sensitive actions:
- Claude moves file to `Pending_Approval/`
- You review and move to `Approved/` or `Rejected/`
- Claude completes the action

## Getting Started

### Start the File Watcher
```bash
python watchers/filesystem_watcher.py
```

### Process Pending Items
```bash
python orchestrator.py
```

### With Claude Code (Interactive)
```bash
claude
# Then ask Claude to process the Needs_Action folder
```

## Daily Workflow

1. **Morning**: Check `Dashboard.md` for overview
2. **During Day**: Drop files in `Inbox/` for processing
3. **Evening**: Review `Pending_Approval/` and approve actions
4. **Weekly**: Read `Briefings/` for CEO summary

## Rules of Engagement

See `Company_Handbook.md` for complete rules. Key points:
- Flag payments > $500 for approval
- Respond to urgent messages within 1 hour
- Document everything in the vault
- Never store passwords or API keys in plain text

---

*Your AI Employee works for you 24/7, 365 days a year.*
