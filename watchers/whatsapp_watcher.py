"""
WhatsApp Watcher for AI Employee.

Monitors WhatsApp Web for new messages and creates action files
in the Needs_Action folder for Claude to process.

Uses Playwright with Chromium for browser automation.
Session data is persisted for quick reconnection.

Authentication:
1. Run: python scripts/whatsapp_init.py
2. Scan QR code with WhatsApp mobile app
3. Session will be saved for future use
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from .base_watcher import BaseWatcher

# Type-only imports for type checkers
if TYPE_CHECKING:
    from playwright.sync_api import Page, Browser, BrowserContext


# Paths
SESSIONS_DIR = Path(__file__).parent.parent / 'sessions'
WHATSAPP_SESSION_DIR = SESSIONS_DIR / 'whatsapp'

# WhatsApp Web URL
WHATSAPP_WEB_URL = 'https://web.whatsapp.com'

# Default keywords to monitor
DEFAULT_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help']


class WhatsAppWatcher(BaseWatcher):
    """
    Watcher that monitors WhatsApp Web for new messages.
    
    Features:
    - Persistent session (scan QR code once)
    - Monitors for urgent keywords
    - Creates action files in Needs_Action folder
    - Auto-reconnect on session expiry
    """
    
    def __init__(
        self, 
        vault_path: str | Path, 
        check_interval: int = 30,
        keywords: list[str] | None = None
    ):
        """
        Initialize the WhatsApp watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 30)
            keywords: List of keywords to monitor (default: urgent, asap, etc.)
        """
        super().__init__(vault_path, check_interval)
        
        self.keywords = keywords or DEFAULT_KEYWORDS
        self.session_dir = WHATSAPP_SESSION_DIR
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.processed_messages: set[str] = set()
        
        # Ensure session directory exists
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Monitoring keywords: {self.keywords}")
    
    def _start_browser(self) -> bool:
        """
        Start Chromium browser with persistent session.
        
        Returns:
            True if browser started successfully, False otherwise
        """
        try:
            # Import playwright here to avoid issues if not installed
            from playwright.sync_api import sync_playwright
            
            playwright = sync_playwright().start()
            
            # Launch Chromium with persistent user data
            self.browser = playwright.chromium.launch_persistent_context(
                user_data_dir=str(self.session_dir),
                headless=True,  # Run in background
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            self.context = self.browser
            self.page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()
            
            self.logger.info("Browser started with persistent session")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            return False
    
    def _navigate_to_whatsapp(self) -> bool:
        """
        Navigate to WhatsApp Web.
        
        Returns:
            True if navigation successful, False otherwise
        """
        if not self.page:
            return False
        
        try:
            self.logger.info(f"Navigating to {WHATSAPP_WEB_URL}")
            self.page.goto(WHATSAPP_WEB_URL, wait_until='networkidle', timeout=60000)
            
            # Wait for chat list or QR code
            time.sleep(5)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to WhatsApp: {e}")
            return False
    
    def _is_authenticated(self) -> bool:
        """
        Check if WhatsApp Web is authenticated (QR code scanned).
        
        Returns:
            True if authenticated, False if QR code needs scanning
        """
        if not self.page:
            return False
        
        try:
            # Check for chat list (authenticated) vs QR code (not authenticated)
            chat_list = self.page.query_selector('[data-testid="chat-list"]')
            qr_code = self.page.query_selector('[data-testid="qr-code"]')
            
            if chat_list:
                self.logger.info("WhatsApp session is authenticated")
                return True
            elif qr_code:
                self.logger.warning("QR code detected - session needs authentication")
                return False
            else:
                # Try another selector
                main_panel = self.page.query_selector('#pane-side')
                if main_panel:
                    self.logger.info("WhatsApp session appears authenticated")
                    return True
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking authentication: {e}")
            return False
    
    def _get_unread_chats(self) -> list:
        """
        Get list of chats with unread messages.
        
        Returns:
            List of chat elements with unread messages
        """
        if not self.page:
            return []
        
        try:
            # Find all chat elements
            chats = []
            
            # Try to find chat elements with unread indicator
            chat_elements = self.page.query_selector_all('[data-testid="chat-list"] > div')
            
            for chat in chat_elements:
                try:
                    # Get chat text content
                    text = chat.inner_text(timeout=2000).lower()
                    
                    # Check for unread indicator
                    unread_badge = chat.query_selector('[aria-label*="unread"]')
                    
                    if unread_badge or any(kw in text for kw in self.keywords):
                        # Extract chat name/number
                        try:
                            name_element = chat.query_selector('[dir="auto"]')
                            name = name_element.inner_text(timeout=2000) if name_element else "Unknown"
                        except:
                            name = "Unknown"
                        
                        chats.append({
                            'name': name,
                            'text': text,
                            'element': chat
                        })
                        
                except Exception:
                    continue
            
            return chats
            
        except Exception as e:
            self.logger.error(f"Error getting unread chats: {e}")
            return []
    
    def check_for_updates(self) -> list:
        """
        Check for new WhatsApp messages with urgent keywords.
        
        Returns:
            List of new messages to process
        """
        if not self.page:
            if not self._start_browser():
                return []
            if not self._navigate_to_whatsapp():
                return []
        
        # Check if still authenticated
        if not self._is_authenticated():
            self.logger.warning("WhatsApp session expired. Please re-authenticate.")
            self.logger.warning("Run: python scripts/whatsapp_init.py")
            return []
        
        try:
            # Get unread chats
            chats = self._get_unread_chats()
            
            # Filter for keywords and new messages
            urgent_messages = []
            for chat in chats:
                # Create unique message ID
                msg_id = f"{chat['name']}_{int(time.time())}"
                
                if msg_id not in self.processed_messages:
                    # Check for keywords
                    if any(keyword in chat['text'] for keyword in self.keywords):
                        urgent_messages.append(chat)
                        self.processed_messages.add(msg_id)
            
            # Limit processed messages set size
            if len(self.processed_messages) > 1000:
                self.processed_messages = set(list(self.processed_messages)[-500:])
            
            return urgent_messages
            
        except Exception as e:
            self.logger.error(f"Error checking WhatsApp messages: {e}")
            return []
    
    def create_action_file(self, chat: dict) -> Path:
        """
        Create a markdown action file for a WhatsApp message.
        
        Args:
            chat: Chat dictionary with name, text, and element
            
        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = ''.join(c for c in chat['name'] if c.isalnum() or c in ' _-')[:30]
        filename = f"WHATSAPP_{timestamp}_{safe_name}.md"
        filepath = self.needs_action / filename
        
        # Determine priority
        priority = 'high' if any(kw in chat['text'].lower() for kw in ['urgent', 'asap', 'emergency']) else 'normal'
        
        # Create markdown content
        content = f'''---
type: whatsapp
from: {chat['name']}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
keywords_detected: {[kw for kw in self.keywords if kw in chat['text'].lower()]}
---

# WhatsApp Message

**From:** {chat['name']}

**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Priority:** {priority.upper()}

---

## Message Content

{chat['text']}

---

## Suggested Actions

- [ ] Read and understand the message
- [ ] Determine if reply is needed
- [ ] Draft reply (if needed)
- [ ] Mark as high priority if urgent
- [ ] Move to /Done when complete

---

## Notes

*This message was imported from WhatsApp Web by AI Employee.*
*Session is maintained for continuous monitoring.*
'''
        
        filepath.write_text(content)
        self.logger.info(f"Created action file for WhatsApp from {chat['name']}")
        
        return filepath
    
    def run(self) -> None:
        """
        Main run loop for the WhatsApp watcher.
        
        Continuously checks for new messages and creates action files.
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info(f'Keywords: {self.keywords}')
        
        # Start browser and navigate
        if not self._start_browser():
            self.logger.error("Failed to start browser. Exiting.")
            return
        
        if not self._navigate_to_whatsapp():
            self.logger.error("Failed to navigate to WhatsApp. Exiting.")
            return
        
        # Check authentication
        if not self._is_authenticated():
            self.logger.error("="*60)
            self.logger.error("QR Code detected - Authentication required")
            self.logger.error("="*60)
            self.logger.error("Please run: python scripts/whatsapp_init.py")
            self.logger.error("This will open a browser for QR code scanning.")
            self.logger.error("="*60)
            
            # Keep running in case user authenticates externally
            # but don't process messages
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} urgent message(s)')
                        for item in items:
                            try:
                                filepath = self.create_action_file(item)
                                self.logger.info(f'Created action file: {filepath.name}')
                            except Exception as e:
                                self.logger.error(f'Error creating action file: {e}')
                    else:
                        self.logger.debug('No new urgent messages')
                except Exception as e:
                    self.logger.error(f'Error checking for updates: {e}')
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        finally:
            # Cleanup
            if self.browser:
                self.browser.close()
                self.logger.info("Browser closed")
