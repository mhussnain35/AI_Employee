# Security & API Keys Documentation

## Silver Tier Security Status ✓

The Silver Tier implementation includes proper security measures for handling API keys and credentials.

---

## Current Implementation

### Credentials Storage

| Service | Credential Type | Location | Git-Safe |
|---------|----------------|----------|----------|
| Gmail API | OAuth2 (credentials.json + token.json) | `credentials/` | ✓ Yes |
| WhatsApp Web | Session cookies | `sessions/whatsapp/` | ✓ Yes |
| Environment Variables | Config values | `.env` | ✓ Yes |

### Protected Files

All sensitive files are excluded from Git via `.gitignore`:

```
.env
credentials/
sessions/
*.json (except package.json)
```

---

## API Keys Required (Silver Tier)

### Gmail API
- **Required:** Yes
- **Type:** OAuth2 credentials
- **Storage:** `credentials/credentials.json` + `credentials/token.json`
- **Get from:** [Google Cloud Console](https://console.cloud.google.com)
- **Setup:** `python main.py setup-gmail`

### WhatsApp Web
- **Required:** No API key
- **Type:** Session-based (QR code)
- **Storage:** `sessions/whatsapp/`
- **Get from:** QR code scan
- **Setup:** `python main.py setup-whatsapp`

---

## Where to Store API Keys

### 1. Environment Variables (`.env` file)

```bash
# .env - NEVER COMMIT TO GIT

# Gmail API
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REDIRECT_URI=http://localhost:8080
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly

# WhatsApp (optional config)
WHATSAPP_KEYWORDS=urgent,asap,invoice,payment,help
WHATSAPP_CHECK_INTERVAL=30
```

### 2. Credentials Folder

```
AI_Employee/
├── credentials/
│   ├── credentials.json  # From Google (git-ignored)
│   └── token.json        # Auto-generated (git-ignored)
```

### 3. Sessions Folder

```
AI_Employee/
├── sessions/
│   └── whatsapp/  # Browser session (git-ignored)
```

---

## Security Best Practices

### 1. Never Commit Secrets

✓ **DO:**
- Store secrets in `.env` files
- Keep credentials in `credentials/` folder
- Use environment variables

✗ **DON'T:**
- Commit `.env` to Git
- Hardcode API keys in Python files
- Share credentials via email/chat

### 2. Use `.env.example` for Templates

A template file `.env.example` is provided with placeholder values:

```bash
# Copy template
cp .env.example .env

# Edit .env with your real credentials
```

### 3. Principle of Least Privilege

The GmailWatcher requests **read-only** access:
- Scope: `https://www.googleapis.com/auth/gmail.readonly`
- Cannot send emails
- Cannot delete emails
- Cannot modify emails

### 4. Token Management

- Tokens auto-refresh when expired
- Backup `credentials/` folder securely
- Revoke access from [Google Security Settings](https://myaccount.google.com/permissions)

---

## WhatsApp Security Notes

### Session Storage
- Session data in `sessions/whatsapp/`
- Excluded from Git
- Contains authentication cookies
- **Do not share** this folder

### Privacy
The WhatsAppWatcher:
- ✓ Reads message text
- ✓ Reads sender name
- ✓ Monitors chat list
- ✗ Cannot send messages
- ✗ Cannot access media
- ✗ Cannot delete messages

### Terms of Service
**Important:** This uses WhatsApp Web automation.
- Review [WhatsApp Terms of Service](https://www.whatsapp.com/legal/terms-of-service)
- Consider official WhatsApp Business API for production

---

## File Permissions

### Recommended Permissions

| File/Folder | Permissions | Reason |
|-------------|-------------|--------|
| `.env` | 600 (rw-------) | Only you can read/write |
| `credentials/` | 700 (rwx------) | Only you can access |
| `sessions/` | 700 (rwx------) | Only you can access |
| `*.py` scripts | 755 (rwxr-xr-x) | Executable |

### Set Permissions (Linux/Mac)

```bash
chmod 600 .env
chmod 700 credentials/
chmod 700 sessions/
```

---

## Audit Logging

All watcher actions are logged with timestamps:

```
2026-03-27 15:33:16 - GmailWatcher - INFO - Connected to Gmail: user@example.com
2026-03-27 15:33:20 - GmailWatcher - INFO - Found 2 new email(s)
2026-03-27 15:33:21 - GmailWatcher - INFO - Created action file: EMAIL_20260327_153321.md
```

Logs include:
- Timestamp
- Watcher name
- Action performed
- File names (not content)

---

## Security Checklist

Before running in production:

- [ ] `.env` file created with credentials
- [ ] `.env` added to `.gitignore`
- [ ] `credentials/` folder secured
- [ ] `sessions/` folder secured
- [ ] File permissions set correctly
- [ ] Google Cloud project secured
- [ ] OAuth2 consent screen configured
- [ ] API keys rotated regularly
- [ ] Monitoring enabled for unusual activity

---

## Incident Response

### If Credentials Are Compromised

1. **Revoke Access Immediately:**
   - Gmail: [Google Security Settings](https://myaccount.google.com/permissions)
   - WhatsApp: Logout all linked devices

2. **Generate New Credentials:**
   - Download new `credentials.json` from Google Cloud
   - Re-run `python main.py setup-gmail`
   - Re-run `python main.py setup-whatsapp`

3. **Audit Logs:**
   - Check for unauthorized access
   - Review action files created
   - Monitor vault for changes

---

## Compliance Notes

### Data Protection
- All data stored locally
- No data sent to external servers (except Gmail API)
- User controls all credentials
- Easy to delete/export data

### GDPR Considerations
- Only process emails you own
- Don't process personal data of others without consent
- Implement right-to-erasure (delete action files on request)

---

## Next Steps (Gold Tier)

Additional security considerations for Gold Tier:

- **Odoo Integration:** Secure API keys for ERP
- **Social Media:** Secure tokens for Facebook/Instagram/Twitter
- **Banking:** Never store banking credentials (use approval workflow only)
- **Cloud Deployment:** Encrypt vault sync, use HTTPS

---

*Security First: Your data and credentials are safe when you follow these practices.*
