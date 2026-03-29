#!/usr/bin/env python3
"""
WhatsApp Session Initialization Script

This script helps you authenticate with WhatsApp Web by scanning
a QR code with your WhatsApp mobile app. The session is then
saved for future use by the WhatsAppWatcher.

Usage:
    python scripts/whatsapp_init.py
    or
    python main.py setup-whatsapp

Instructions:
1. Run this script
2. A browser window will open showing WhatsApp Web
3. Open WhatsApp on your phone
4. Go to Settings → Linked Devices → Link a Device
5. Scan the QR code shown in the browser
6. Session will be saved automatically
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# Paths
SESSIONS_DIR = Path(__file__).parent.parent / 'sessions'
WHATSAPP_SESSION_DIR = SESSIONS_DIR / 'whatsapp'

# WhatsApp Web URL
WHATSAPP_WEB_URL = 'https://web.whatsapp.com'


def setup_session_dir() -> None:
    """Create session directory if it doesn't exist."""
    WHATSAPP_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Session directory: {WHATSAPP_SESSION_DIR}")


def authenticate() -> bool:
    """
    Authenticate with WhatsApp Web by scanning QR code.
    
    Returns:
        True if authentication successful, False otherwise
    """
    print("\n" + "="*60)
    print("WhatsApp Web Authentication")
    print("="*60)
    print("\nThis will open Chrome browser with WhatsApp Web.")
    print("\nSteps to authenticate:")
    print("1. Wait for the QR code to appear")
    print("2. Open WhatsApp on your phone")
    print("3. Go to Settings → Linked Devices")
    print("4. Tap 'Link a Device'")
    print("5. Scan the QR code shown in the browser")
    print("\nWaiting for Chrome to open...\n")

    try:
        # Import playwright here to avoid module import errors
        from playwright.sync_api import sync_playwright
        
        playwright = sync_playwright().start()

        # Launch Chrome browser with persistent context
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(WHATSAPP_SESSION_DIR),
            headless=False,  # Show browser for QR code scanning
            channel='chrome',  # Use Google Chrome specifically
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ],
            timeout=60000
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        print("Navigating to WhatsApp Web...")
        try:
            page.goto(WHATSAPP_WEB_URL, wait_until='networkidle', timeout=60000)
        except Exception as e:
            print(f"Warning: Page load issue: {e}")
            print("Continuing anyway...")

        print("\n" + "="*60)
        print("Please scan the QR code with your WhatsApp mobile app")
        print("="*60)
        print("\nMonitoring for authentication (2 minutes max)...")

        # Monitor for authentication
        max_wait_time = 120  # 2 minutes
        start_time = time.time()
        authenticated = False

        while time.time() - start_time < max_wait_time:
            try:
                # Check for chat list (authenticated)
                chat_list = page.query_selector('[data-testid="chat-list"]')

                if chat_list:
                    print("\n\n✓ Authentication successful!")
                    authenticated = True
                    break

                # Check if QR code is visible
                qr_code = page.query_selector('[data-testid="qr-code"]')
                if qr_code:
                    # Show progress
                    elapsed = int(time.time() - start_time)
                    remaining = max_wait_time - elapsed
                    if elapsed % 10 == 0:  # Show message every 10 seconds
                        print(f"  Waiting for QR scan... ({remaining}s remaining)")
                    time.sleep(2)
                else:
                    # Page might still be loading
                    print("Waiting for WhatsApp Web to load...")
                    time.sleep(3)

            except Exception as e:
                print(f"Checking authentication... ({e})")
                time.sleep(2)

        if not authenticated:
            print("\n\n⚠ Authentication timeout after 2 minutes")
            print("\nPossible reasons:")
            print("  1. QR code expired (they refresh every ~60 seconds)")
            print("  2. QR code was not scanned")
            print("  3. Network connection issue")
            print("\nThe session may still have been saved if you scanned.")
            print("Try running the script again if authentication failed.")
        else:
            print("\nSession will be saved automatically.")

        # Keep browser open for a few more seconds
        time.sleep(3)

        # Close browser
        browser.close()
        playwright.stop()

        return authenticated

    except KeyboardInterrupt:
        print("\n\n✗ Authentication cancelled by user")
        return False
    except Exception as e:
        print(f"\n✗ Error during authentication: {e}")
        print("\nCommon issues:")
        print("  1. Chrome not installed - install Google Chrome browser")
        print("  2. Playwright not installed - run: playwright install chromium")
        print("  3. Browser launch failed - try running as administrator")
        print("  4. Network issue - check internet connection")
        print("\nTry again: python main.py setup-whatsapp")
        return False


def test_session() -> bool:
    """
    Test if the saved session is valid.
    
    Returns:
        True if session is valid, False otherwise
    """
    print("\nTesting saved session...")
    
    try:
        playwright = sync_playwright().start()
        
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(WHATSAPP_SESSION_DIR),
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(WHATSAPP_WEB_URL, wait_until='networkidle', timeout=30000)
        
        # Wait a bit for page to load
        time.sleep(5)
        
        # Check for chat list
        chat_list = page.query_selector('[data-testid="chat-list"]')
        is_authenticated = chat_list is not None
        
        browser.close()
        playwright.stop()
        
        if is_authenticated:
            print("✓ Session is valid and authenticated")
        else:
            print("⚠ Session may need re-authentication")
        
        return is_authenticated
        
    except Exception as e:
        print(f"✗ Session test failed: {e}")
        return False


def main():
    """Main entry point."""
    print("="*60)
    print("WhatsApp Session Initialization")
    print("="*60)
    
    # Setup
    setup_session_dir()
    
    # Authenticate
    success = authenticate()
    
    if success:
        # Test the session
        print("\n" + "="*60)
        test_session()
        
        print("\n" + "="*60)
        print("WhatsApp Authentication Complete!")
        print("="*60)
        print(f"\nSession saved to: {WHATSAPP_SESSION_DIR}")
        print("This session will be used automatically by WhatsAppWatcher.")
        print("\nNext steps:")
        print("1. Run: python main.py watcher-whatsapp")
        print("2. Or run: python main.py watcher-all (all watchers)")
        print("\nNote: Session typically lasts for several days.")
        print("If WhatsAppWatcher stops detecting messages, re-run this script.")
    else:
        print("\n" + "="*60)
        print("Authentication was not completed")
        print("="*60)
        print("\nYou can try again by running: python scripts/whatsapp_init.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
