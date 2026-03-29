# AI Brain Configuration Guide

## 🧠 Overview

The AI Employee now has a **Brain** - an AI reasoning engine that can process tasks, create intelligent plans, and make decisions. You can choose between two AI backends:

1. **Claude Code** (CLI-based, by Anthropic)
2. **Qwen** (API-based, by Alibaba)

---

## ⚡ Quick Start

### Option 1: Use Claude Code (Recommended)

**1. Install Claude Code CLI:**
```bash
# Download from: https://claude.com/claude-code
# Follow installation instructions
```

**2. Authenticate:**
```bash
claude login
```

**3. Configure .env:**
```bash
AI_BRAIN=claude
CLAUDE_MODEL=claude-sonnet-4-20250514
```

**4. Test:**
```bash
python test_ai_brain.py
```

---

### Option 2: Use Qwen API

**1. Get API Key:**
- Go to: https://dashscope.aliyun.com/
- Sign up / Log in
- Create API key

**2. Configure .env:**
```bash
AI_BRAIN=qwen
QWEN_API_KEY=sk-your-actual-api-key-here
QWEN_MODEL=qwen-plus
```

**3. Test:**
```bash
python test_ai_brain.py
```

---

## 📋 Configuration Reference

### .env File Settings

```bash
# ===========================================
# AI Brain Selection (REQUIRED)
# ===========================================
# Choose ONE: "claude" or "qwen"
AI_BRAIN=claude

# ===========================================
# Claude Configuration (if AI_BRAIN=claude)
# ===========================================
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4096
CLAUDE_TIMEOUT=300

# Optional: Claude API (alternative to CLI)
# CLAUDE_API_KEY=your-api-key
# CLAUDE_BASE_URL=https://api.anthropic.com

# ===========================================
# Qwen Configuration (if AI_BRAIN=qwen)
# ===========================================
QWEN_API_KEY=your-api-key-here
QWEN_MODEL=qwen-plus  # Options: qwen-plus, qwen-max, qwen-turbo
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MAX_TOKENS=4096
QWEN_TIMEOUT=300
```

---

## 🎯 How to Switch Brains

### From Claude to Qwen:

**1. Edit .env:**
```bash
# Change this:
AI_BRAIN=claude

# To this:
AI_BRAIN=qwen

# And add your Qwen API key:
QWEN_API_KEY=sk-your-key
```

**2. Restart the system:**
```bash
python run_system.py
```

### From Qwen to Claude:

**1. Edit .env:**
```bash
# Change this:
AI_BRAIN=qwen

# To this:
AI_BRAIN=claude

# Make sure Claude Code CLI is installed
```

**2. Restart the system:**
```bash
python run_system.py
```

---

## 🧪 Testing

### Test Environment Configuration:
```bash
python test_ai_brain.py
```

**Expected Output:**
```
✓ Environment Configuration
✓ Claude Processor (if CLI installed)
✓ Qwen Processor (if API key set)
✓ AI Brain Interface
✓ Ralph Wiggum Loop
✓ Orchestrator Integration
```

### Test Specific Brain:

**Test Claude:**
```bash
python -c "from claude_processor import ClaudeProcessor; p = ClaudeProcessor(); print('OK' if p.is_available() else 'NOT AVAILABLE')"
```

**Test Qwen:**
```bash
python -c "from qwen_processor import QwenProcessor; p = QwenProcessor(); print('OK' if p.is_available() else 'NOT AVAILABLE')"
```

---

## 📊 Comparison: Claude vs Qwen

| Feature | Claude Code | Qwen API |
|---------|-------------|----------|
| **Type** | CLI + API | API only |
| **Setup** | Install CLI | Get API key |
| **Cost** | Subscription | Pay-per-use |
| **Speed** | Fast (local) | Fast (cloud) |
| **Context** | 200K tokens | 32K tokens |
| **Best For** | Complex reasoning | Cost-effective |

---

## 🔧 Troubleshooting

### Claude Not Available

**Error:** `Claude Code CLI not found`

**Solution:**
```bash
# 1. Install Claude Code
# Visit: https://claude.com/claude-code

# 2. Verify installation
claude --version

# 3. Login
claude login

# 4. Test
python -c "from claude_processor import ClaudeProcessor; print(ClaudeProcessor().is_available())"
```

---

### Qwen Not Available

**Error:** `QWEN_API_KEY not set`

**Solution:**
```bash
# 1. Get API key from: https://dashscope.aliyun.com/

# 2. Add to .env:
QWEN_API_KEY=sk-your-key

# 3. Test
python -c "from qwen_processor import QwenProcessor; print(QwenProcessor().is_available())"
```

---

### AI Brain Not Processing

**Error:** `AI Brain processor not initialized`

**Solution:**
```bash
# 1. Check .env file exists
# 2. Verify AI_BRAIN setting
# 3. Run test suite
python test_ai_brain.py

# 4. Check logs for errors
```

---

## 📖 What the Brain Does

### 1. **Intelligent Plan Creation**

**Before (Template):**
```markdown
- [ ] Review the item content
- [ ] Determine priority level
- [ ] Identify required actions
```

**After (AI-Generated):**
```markdown
## Priority: HIGH
**Reason:** Email contains "urgent" and is from VIP contact

## Actions:
- [ ] Reply to boss@company.com within 1 hour (per Company Handbook)
- [ ] Forward to team if requires group action
- [ ] Schedule follow-up in calendar
```

---

### 2. **Item Classification**

The AI automatically classifies items:
- **Type:** email, whatsapp, file_drop, etc.
- **Priority:** critical, high, normal, low
- **Category:** communication, finance, task, etc.
- **Approval Required:** true/false (for payments > $500)

---

### 3. **Ralph Wiggum Persistence Loop**

The AI keeps working until tasks are complete:
- Monitors task completion
- Retries on failure
- Respects max iterations
- Logs all attempts

---

## 🚀 Usage Examples

### Process Items with AI:

```bash
# Process all pending items
python main.py process

# Process without AI (template mode)
python main.py process --no-ai

# Process specific vault
python main.py process /path/to/vault
```

### In Python Code:

```python
from ai_brain import AIBrain

# Initialize brain
brain = AIBrain()  # Reads AI_BRAIN from .env

# Process prompt
response = brain.process("What tasks need attention?")

# Create plan
plan = brain.create_plan(
    item_content="Urgent: Pay invoice $600",
    handbook_content="Flag payments > $500 for approval",
    item_path=Path("Needs_Action/INVOICE.md")
)

# Classify item
classification = brain.classify_item(email_content)
print(classification['priority'])  # "high"
```

---

## 📁 File Structure

```
AI_Employee/
├── ai_brain.py              # Main AI brain interface
├── claude_processor.py      # Claude Code integration
├── qwen_processor.py        # Qwen API integration
├── ralph_wiggum.py          # Persistence loop
├── orchestrator.py          # Uses AI brain
├── .env                     # Configuration (YOU EDIT THIS)
├── .env.example             # Template
└── test_ai_brain.py         # Test suite
```

---

## 🎯 Next Steps

After configuring the AI Brain:

1. **Test the setup:**
   ```bash
   python test_ai_brain.py
   ```

2. **Process items:**
   ```bash
   python main.py process
   ```

3. **Run the full system:**
   ```bash
   python run_system.py
   ```

4. **Monitor logs:**
   - Check terminal output
   - Review Plans/ folder for AI-generated plans
   - Verify classifications are correct

---

## 📚 Additional Resources

- **Claude Code:** https://claude.com/claude-code
- **Qwen API:** https://dashscope.aliyun.com/
- **Ralph Wiggum Pattern:** https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum

---

## ✅ Checklist

**Claude Setup:**
- [ ] Claude Code CLI installed
- [ ] Authenticated with `claude login`
- [ ] AI_BRAIN=claude in .env
- [ ] Test passes: `python test_ai_brain.py`

**Qwen Setup:**
- [ ] API key obtained from Alibaba Cloud
- [ ] QWEN_API_KEY set in .env
- [ ] AI_BRAIN=qwen in .env
- [ ] Test passes: `python test_ai_brain.py`

---

**Your AI Employee now has a working Brain!** 🧠🎉

Choose your AI backend, configure .env, and watch it intelligently process tasks!
