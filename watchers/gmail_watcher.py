"""
Gmail Watcher for AI Employee.

Monitors Gmail for new emails and creates action files
in the Needs_Action folder for Claude to process.

Authentication:
1. Run: python scripts/gmail_auth.py
2. Follow browser prompts to authenticate
3. token.json will be created automatically
"""

import base64
from datetime import datetime
from email import message_from_bytes
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .base_watcher import BaseWatcher


# Paths
CREDENTIALS_DIR = Path(__file__).parent.parent / 'credentials'
CREDENTIALS_FILE = CREDENTIALS_DIR / 'credentials.json'
TOKEN_FILE = CREDENTIALS_DIR / 'token.json'


class GmailWatcher(BaseWatcher):
    """
    Watcher that monitors Gmail for new emails.
    
    Features:
    - Monitors unread and important emails
    - Creates action files in Needs_Action folder
    - Tracks processed message IDs to avoid duplicates
    - Auto-refreshes expired tokens
    """
    
    def __init__(self, vault_path: str | Path, check_interval: int = 120):
        """
        Initialize the Gmail watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        self.service: Optional[build] = None
        self.processed_ids: set[str] = set()
        self.credentials: Optional[Credentials] = None
        
        # Load credentials
        self._load_credentials()
    
    def _load_credentials(self) -> bool:
        """
        Load Gmail credentials and create API service.
        
        Returns:
            True if credentials loaded successfully, False otherwise
        """
        try:
            if not TOKEN_FILE.exists():
                self.logger.error(f"Token file not found: {TOKEN_FILE}")
                self.logger.error("Run: python scripts/gmail_auth.py to authenticate")
                return False
            
            # Load credentials from token file
            self.credentials = Credentials.from_authorized_user_file(
                TOKEN_FILE, 
                ['https://www.googleapis.com/auth/gmail.readonly']
            )
            
            # Refresh if expired
            if self.credentials.expired and self.credentials.refresh_token:
                self.logger.info("Refreshing expired token...")
                self.credentials.refresh(Request())
                
                # Save refreshed token
                with open(TOKEN_FILE, 'w') as token:
                    token.write(self.credentials.to_json())
                self.logger.info("Token refreshed and saved")
            
            # Build Gmail API service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            
            # Test connection
            profile = self.service.users().getProfile(userId='me').execute()
            email = profile.get('emailAddress')
            self.logger.info(f"Connected to Gmail: {email}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load credentials: {e}")
            self.logger.error("Run: python scripts/gmail_auth.py to re-authenticate")
            return False
    
    def check_for_updates(self) -> list:
        """
        Check for new unread and important emails.
        
        Returns:
            List of new message IDs to process
        """
        if not self.service:
            if not self._load_credentials():
                return []
        
        try:
            # Search for unread, important messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            # Filter out already processed messages
            new_messages = [
                msg for msg in messages 
                if msg['id'] not in self.processed_ids
            ]
            
            return new_messages
            
        except HttpError as e:
            if e.resp.status == 401:
                self.logger.warning("Authentication failed, trying to refresh...")
                self._load_credentials()
            else:
                self.logger.error(f"Gmail API error: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []
    
    def _get_message(self, message_id: str) -> dict:
        """
        Get full message details from Gmail API.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary with message details
        """
        raw_message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='raw'
        ).execute()
        
        # Decode message
        message_bytes = base64.urlsafe_b64decode(raw_message['raw'])
        mime_msg = message_from_bytes(message_bytes)
        
        # Extract headers
        headers = {}
        for header in ['From', 'To', 'Subject', 'Date']:
            headers[header] = mime_msg.get(header, '')
        
        # Get message body
        body = self._get_message_body(mime_msg)
        
        return {
            'id': message_id,
            'headers': headers,
            'body': body,
            'snippet': raw_message.get('snippet', '')
        }
    
    def _get_message_body(self, mime_msg) -> str:
        """
        Extract the body text from an email message.
        
        Args:
            mime_msg: Parsed email message
            
        Returns:
            Message body text
        """
        body = ""
        
        # Try multipart first
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition") or "")
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                # Prefer plain text
                if content_type == "text/plain":
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        body = part.get_payload(decode=True).decode(charset, errors='replace')
                        break
                    except:
                        continue
        else:
            # Simple message
            try:
                charset = mime_msg.get_content_charset() or 'utf-8'
                body = mime_msg.get_payload(decode=True).decode(charset, errors='replace')
            except:
                body = mime_msg.get_payload()
        
        return body
    
    def create_action_file(self, message: dict) -> Path:
        """
        Create a markdown action file for an email.
        
        Args:
            message: Gmail message dictionary
            
        Returns:
            Path to created action file
        """
        # Get full message details
        msg_details = self._get_message(message['id'])
        headers = msg_details['headers']
        
        # Generate filename
        subject = headers.get('Subject', 'No Subject')[:50].replace(' ', '_')
        subject = ''.join(c for c in subject if c.isalnum() or c in '_-')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"EMAIL_{timestamp}_{subject}.md"
        filepath = self.needs_action / filename
        
        # Determine priority
        priority = 'high' if 'important' in str(headers).lower() else 'normal'
        
        # Create markdown content
        content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
to: {headers.get('To', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
gmail_id: {message['id']}
---

# Email: {headers.get('Subject', 'No Subject')}

**From:** {headers.get('From', 'Unknown')}

**To:** {headers.get('To', 'Unknown')}

**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Priority:** {priority.upper()}

---

## Email Content

{msg_details['body'][:2000] if msg_details['body'] else msg_details['snippet']}

---

## Suggested Actions

- [ ] Read and understand the email
- [ ] Determine if reply is needed
- [ ] Draft reply (if needed)
- [ ] Forward to relevant party (if needed)
- [ ] Archive after processing
- [ ] Move to /Done when complete

---

## Notes

*This email was imported from Gmail by AI Employee.*
*Mark as read in Gmail after processing if needed.*
'''
        
        filepath.write_text(content)
        self.processed_ids.add(message['id'])
        
        self.logger.info(f"Created action file for email from {headers.get('From', 'Unknown')}")
        
        return filepath
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a Gmail message as read.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            return False
        
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            self.logger.debug(f"Marked message {message_id} as read")
            return True
        except Exception as e:
            self.logger.error(f"Failed to mark message as read: {e}")
            return False
    
    def run(self) -> None:
        """
        Main run loop for the Gmail watcher.
        
        Continuously checks for new emails and creates action files.
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        if not self.service:
            if not self._load_credentials():
                self.logger.error("Failed to initialize Gmail API. Exiting.")
                return
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} new email(s)')
                        for item in items:
                            try:
                                filepath = self.create_action_file(item)
                                self.logger.info(f'Created action file: {filepath.name}')
                                
                                # Optionally mark as read
                                # self.mark_as_read(item['id'])
                            except Exception as e:
                                self.logger.error(f'Error creating action file: {e}')
                    else:
                        self.logger.debug('No new emails')
                except Exception as e:
                    self.logger.error(f'Error checking for updates: {e}')
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')


# Import time here to avoid circular dependency
import time
