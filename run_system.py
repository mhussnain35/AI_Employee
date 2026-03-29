#!/usr/bin/env python3
"""
AI Employee - Main System Runner

This is the main entry point to start your AI Employee system.
It initializes all components, checks authentication, and starts
all watchers with the orchestrator.

Usage:
    python run_system.py

Or simply:
    python main.py
"""

import sys
import time
import threading
from pathlib import Path
from datetime import datetime


def print_banner():
    """Print the AI Employee banner."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║           AI Employee - Your Digital FTE                 ║
║  Local-first, Agent-driven, Human-in-the-loop            ║
║                                                          ║
║  Tier: Silver (Gmail + WhatsApp + FileSystem)            ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_section(text: str):
    """Print a section header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def check_vault(vault_path: Path) -> bool:
    """Check if Obsidian vault exists and is properly configured."""
    print_section("Step 1: Checking Obsidian Vault")
    
    if not vault_path.exists():
        print(f"  ✗ Vault not found at: {vault_path}")
        print("\n  Creating vault structure...")
        from setup_vault import setup_vault
        setup_vault(vault_path)
        print("  ✓ Vault created!")
        return True
    
    # Check required folders
    required_folders = [
        'Inbox',
        'Needs_Action',
        'Done',
        'Plans',
        'Pending_Approval'
    ]
    
    all_exist = True
    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists():
            print(f"  ✓ {folder}/")
        else:
            print(f"  ✗ {folder}/ - Missing")
            all_exist = False
    
    # Check required files
    print("\n  Checking key files:")
    required_files = ['Dashboard.md', 'Company_Handbook.md']
    
    for filename in required_files:
        filepath = vault_path / filename
        if filepath.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - Missing")
            all_exist = False
    
    if all_exist:
        print("\n  ✓ Obsidian Vault is ready!")
    else:
        print("\n  ⚠ Some vault components missing. Run: python main.py setup")
    
    return all_exist


def check_gmail_auth(credentials_dir: Path) -> bool:
    """Check if Gmail is authenticated."""
    print_section("Step 2: Checking Gmail Authentication")
    
    creds_file = credentials_dir / 'credentials.json'
    token_file = credentials_dir / 'token.json'
    
    if not creds_file.exists():
        print(f"  ✗ credentials.json not found")
        print("\n  FIX: Run 'python main.py setup-gmail'")
        return False
    
    if not token_file.exists():
        print(f"  ✗ token.json not found (not authenticated)")
        print("\n  FIX: Run 'python main.py setup-gmail'")
        return False
    
    # Try to load and validate token
    try:
        import json
        token_data = json.loads(token_file.read_text())
        
        # Check expiry
        expiry = token_data.get('expiry', 0)
        import time
        if expiry and expiry < time.time() * 1000:
            print(f"  ⚠ Token expired (will auto-refresh)")
        else:
            print(f"  ✓ Token is valid")
        
        print(f"  ✓ Gmail is authenticated!")
        return True
        
    except Exception as e:
        print(f"  ⚠ Token issue: {e}")
        print("\n  FIX: Run 'python main.py setup-gmail'")
        return False


def check_whatsapp_auth(sessions_dir: Path) -> bool:
    """Check if WhatsApp is authenticated."""
    print_section("Step 3: Checking WhatsApp Authentication")
    
    whatsapp_session = sessions_dir / 'whatsapp'
    cookies_file = whatsapp_session / 'Cookies'
    
    if not cookies_file.exists():
        print(f"  ⚠ No WhatsApp session found")
        print("\n  To authenticate: Run 'python main.py setup-whatsapp'")
        print("  (WhatsApp will work in background mode without session)")
        return False
    
    # Try to test the session
    try:
        from playwright.sync_api import sync_playwright
        
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(whatsapp_session),
            headless=True,
            timeout=10000
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=30000)
        time.sleep(3)
        
        chat_list = page.query_selector('[data-testid="chat-list"]')
        browser.close()
        playwright.stop()
        
        if chat_list:
            print(f"  ✓ WhatsApp session is active!")
            return True
        else:
            print(f"  ⚠ WhatsApp session may be expired")
            print("\n  To re-authenticate: Run 'python main.py setup-whatsapp'")
            return False
            
    except Exception as e:
        print(f"  ⚠ Session test failed: {e}")
        print("\n  To authenticate: Run 'python main.py setup-whatsapp'")
        return False


def start_file_watcher(vault_path: Path):
    """Start the File System Watcher."""
    from watchers import FileSystemWatcher
    
    print("\n  Starting File System Watcher...")
    watcher = FileSystemWatcher(vault_path, check_interval=5)
    
    # Run in a thread
    thread = threading.Thread(target=watcher.run, daemon=True)
    thread.start()
    
    print("  ✓ File System Watcher started (checking every 5s)")
    return watcher


def start_gmail_watcher(vault_path: Path, gmail_auth: bool):
    """Start the Gmail Watcher if authenticated."""
    if not gmail_auth:
        print("\n  ⊘ Gmail Watcher: Skipped (not authenticated)")
        print("     Run 'python main.py setup-gmail' to enable")
        return None
    
    try:
        from watchers import GmailWatcher
        
        print("\n  Starting Gmail Watcher...")
        watcher = GmailWatcher(vault_path, check_interval=120)
        
        # Check if Gmail API is accessible
        if watcher.service:
            # Run in a thread
            thread = threading.Thread(target=watcher.run, daemon=True)
            thread.start()
            print("  ✓ Gmail Watcher started (checking every 2m)")
            return watcher
        else:
            print("  ⊘ Gmail Watcher: Skipped (API not accessible)")
            return None
            
    except Exception as e:
        print(f"  ⊘ Gmail Watcher: Skipped ({e})")
        return None


def start_whatsapp_watcher(vault_path: Path, whatsapp_auth: bool):
    """Start the WhatsApp Watcher if authenticated."""
    if not whatsapp_auth:
        print("\n  ⊘ WhatsApp Watcher: Skipped (not authenticated)")
        print("     Run 'python main.py setup-whatsapp' to enable")
        return None
    
    try:
        from watchers import WhatsAppWatcher
        
        print("\n  Starting WhatsApp Watcher...")
        watcher = WhatsAppWatcher(vault_path, check_interval=30)
        
        # Run in a thread
        thread = threading.Thread(target=watcher.run, daemon=True)
        thread.start()
        print("  ✓ WhatsApp Watcher started (checking every 30s)")
        return watcher
        
    except Exception as e:
        print(f"  ⊘ WhatsApp Watcher: Skipped ({e})")
        return None


def start_orchestrator(vault_path: Path):
    """Start the orchestrator to process pending items."""
    from orchestrator import Orchestrator

    print_section("Step 5: Starting Orchestrator")
    
    # Check AI Brain status
    print("\n  Checking AI Brain...")
    try:
        from ai_brain import AIBrain
        brain = AIBrain()
        print(f"  ✓ AI Brain initialized: {brain.brain_type}")
        print(f"  ✓ Processor: {type(brain.processor).__name__}")
        use_ai = True
    except Exception as e:
        print(f"  ⚠ AI Brain not available: {e}")
        print(f"  ⊘ Using template-based processing")
        use_ai = False

    orchestrator = Orchestrator(vault_path, use_ai=use_ai)

    # Process any pending items
    pending = orchestrator.get_pending_items()

    if pending:
        print(f"\n  Found {len(pending)} pending item(s)")
        orchestrator.run()
    else:
        print("\n  ✓ No pending items to process")

    return orchestrator


def print_status(vault_path: Path, watchers: dict):
    """Print the current system status."""
    print_section("System Status")

    print(f"\n  Vault: {vault_path}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show AI Brain status
    print("\n  AI Brain:")
    try:
        from ai_brain import AIBrain
        brain = AIBrain()
        print(f"    ✓ Type: {brain.brain_type}")
        print(f"    ✓ Processor: {type(brain.processor).__name__}")
    except:
        print(f"    ⊘ Not configured (using templates)")

    print("\n  Active Watchers:")
    if watchers.get('file'):
        print("    ✓ File System Watcher")
    if watchers.get('gmail'):
        print("    ✓ Gmail Watcher")
    if watchers.get('whatsapp'):
        print("    ✓ WhatsApp Watcher")

    # Count items
    needs_action = len(list((vault_path / 'Needs_Action').glob('*.md')))
    plans = len(list((vault_path / 'Plans').glob('*.md')))
    done = len(list((vault_path / 'Done').glob('*.md')))

    print(f"\n  Items:")
    print(f"    • Needs Action: {needs_action}")
    print(f"    • Plans: {plans}")
    print(f"    • Done: {done}")

    print("\n" + "="*70)
    print("✓ AI Employee System is RUNNING!")
    print("="*70)
    print("\n  Monitoring for new items...")
    print("  Press Ctrl+C to stop\n")


def main():
    """Main entry point for AI Employee system."""
    print_banner()
    
    # Paths
    base_path = Path(__file__).parent
    vault_path = base_path / "AI_Employee_Vault"
    credentials_dir = base_path / "credentials"
    sessions_dir = base_path / "sessions"
    
    # Ensure directories exist
    credentials_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Check vault
    vault_ok = check_vault(vault_path)
    
    if not vault_ok:
        print("\n⚠ Vault setup incomplete. Run: python main.py setup")
        sys.exit(1)
    
    # Step 2: Check Gmail auth
    gmail_auth = check_gmail_auth(credentials_dir)
    
    # Step 3: Check WhatsApp auth
    whatsapp_auth = check_whatsapp_auth(sessions_dir)
    
    # Step 4: Start watchers
    print_section("Step 4: Starting Watchers")
    
    watchers = {}
    
    # File System Watcher (always runs)
    watchers['file'] = start_file_watcher(vault_path)
    
    # Gmail Watcher (if authenticated)
    watchers['gmail'] = start_gmail_watcher(vault_path, gmail_auth)
    
    # WhatsApp Watcher (if authenticated)
    watchers['whatsapp'] = start_whatsapp_watcher(vault_path, whatsapp_auth)
    
    # Step 5: Start orchestrator
    orchestrator = start_orchestrator(vault_path)
    
    # Print status
    print_status(vault_path, watchers)
    
    # Keep system running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Shutting down AI Employee System...")
        print("="*70)
        print("\n  Stopping watchers...")
        print("  ✓ File System Watcher stopped")
        if watchers.get('gmail'):
            print("  ✓ Gmail Watcher stopped")
        if watchers.get('whatsapp'):
            print("  ✓ WhatsApp Watcher stopped")
        print("\n  System stopped gracefully")
        print("\n  To restart: python run_system.py")
        print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ System error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check error messages above")
        print("  2. Run: python main.py status")
        print("  3. Run: python test_simple.py")
        print("\nFor help, see: QUICK_AUTH.md or TESTING_GUIDE.md")
        sys.exit(1)
