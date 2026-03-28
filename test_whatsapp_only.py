#!/usr/bin/env python3
"""
WhatsApp Watcher Test Script - Check Only

This script tests ONLY the WhatsApp Watcher functionality.
No authentication prompts - just checks if everything is ready.

Usage:
    python test_whatsapp_only.py
"""

import sys
import time
from pathlib import Path
from datetime import datetime


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def test_playwright():
    """Test that Playwright is installed."""
    print_header("Step 1: Checking Playwright")
    
    try:
        from playwright.sync_api import sync_playwright
        print("  ✓ playwright.sync_api")
        
        # Test if Chromium is installed
        try:
            playwright = sync_playwright().start()
            print("  ✓ Playwright initialized")
            
            # Try to launch Chromium
            try:
                browser = playwright.chromium.launch(headless=True, timeout=10000)
                print("  ✓ Chromium browser available")
                browser.close()
                playwright.stop()
                print("\n✓ Playwright and Chromium are ready!")
                return True
            except Exception as e:
                print(f"  ✗ Chromium not installed: {e}")
                print("\n  FIX: Install Chromium browser")
                print("  → playwright install chromium")
                playwright.stop()
                return False
                
        except Exception as e:
            print(f"  ✗ Playwright initialization failed: {e}")
            print("\n  FIX: Reinstall Playwright")
            print("  → uv sync")
            return False
            
    except ImportError as e:
        print(f"  ✗ Playwright not installed: {e}")
        print("\n  FIX: Install Playwright")
        print("  → uv add playwright")
        return False


def test_session_directory():
    """Test that session directory exists."""
    print_header("Step 2: Checking Session Directory")
    
    session_dir = Path(__file__).parent / 'sessions' / 'whatsapp'
    
    if session_dir.exists():
        print(f"  ✓ Session directory exists")
        
        # Check for session data
        cookies_file = session_dir / 'Cookies'
        if cookies_file.exists():
            print(f"  ✓ Session cookies found")
        else:
            print(f"  ⊘ No session cookies (need to authenticate)")
        
        print("\n✓ Session directory is ready!")
        return True
    else:
        print(f"  ✓ Session directory will be created on first use")
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {session_dir}")
        return True


def test_watcher_import():
    """Test that WhatsAppWatcher can be imported."""
    print_header("Step 3: Testing WhatsAppWatcher")
    
    try:
        from watchers import WhatsAppWatcher
        print("  ✓ WhatsAppWatcher imported successfully")
        
        vault_path = Path(__file__).parent / "AI_Employee_Vault"
        watcher = WhatsAppWatcher(vault_path, check_interval=30)
        print("  ✓ WhatsAppWatcher instance created")
        
        # Check methods
        methods = ['_start_browser', '_navigate_to_whatsapp', '_is_authenticated', 'create_action_file']
        for method in methods:
            if hasattr(watcher, method):
                print(f"  ✓ Method: {method}")
            else:
                print(f"  ✗ Method missing: {method}")
                return False
        
        # Check keywords
        print(f"  ✓ Monitoring keywords: {watcher.keywords}")
        
        print("\n✓ WhatsAppWatcher code is working!")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n  FIX: Check error message above")
        return False


def check_session_status():
    """Check if WhatsApp session is already authenticated."""
    print_header("Step 4: Checking Session Status")
    
    session_dir = Path(__file__).parent / 'sessions' / 'whatsapp'
    cookies_file = session_dir / 'Cookies'
    
    if not cookies_file.exists():
        print(f"  ✗ No session found (not authenticated)")
        print("\n  FIX: Authenticate WhatsApp")
        print("  → python main.py setup-whatsapp")
        return False
    
    # Try to test the session
    print("  Testing existing session...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        playwright = sync_playwright().start()
        
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=True,
            timeout=30000
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("  Navigating to WhatsApp Web...")
        page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=60000)
        
        time.sleep(5)
        
        # Check if authenticated
        chat_list = page.query_selector('[data-testid="chat-list"]')
        
        if chat_list:
            print("  ✓ Session is authenticated and working!")
            browser.close()
            playwright.stop()
            print("\n✓ WhatsApp is ready!")
            print("  → Run: python main.py watcher-whatsapp")
            return True
        else:
            print("  ⚠ Session may be expired")
            browser.close()
            playwright.stop()
            print("\n  FIX: Re-authenticate WhatsApp")
            print("  → python main.py setup-whatsapp")
            return False
            
    except Exception as e:
        print(f"  ✗ Session test failed: {e}")
        print("\n  FIX: Authenticate WhatsApp")
        print("  → python main.py setup-whatsapp")
        return False


def main():
    """Run all WhatsApp tests."""
    print_header("WhatsApp Watcher Test Suite")
    print("Checking WhatsApp Integration Status")
    print_header("Running Tests...")
    
    # Run tests
    tests = [
        ("Playwright", test_playwright),
        ("Session Directory", test_session_directory),
        ("Watcher Import", test_watcher_import),
        ("Session Status", check_session_status),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\n✗ {name} failed: {e}")
            results.append((name, "FAIL"))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result == "PASS")
    failed = sum(1 for _, result in results if result == "FAIL")
    total = len(results)
    
    for name, result in results:
        if result == "PASS":
            print(f"  ✓ PASS: {name}")
        else:
            print(f"  ✗ FAIL: {name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    
    # Next steps
    print_header("Next Steps")
    
    session_ok = any("Session Status" in name and result == "PASS" 
                     for name, result in results)
    
    if failed > 0:
        print("\n✗ Some tests failed - fix the errors above")
        
    elif not session_ok:
        print("\n⚠ WhatsApp is not authenticated yet")
        print("\nAuthenticate WhatsApp:")
        print("  → python main.py setup-whatsapp")
        print("\nSteps:")
        print("  1. Browser will open with WhatsApp Web")
        print("  2. QR code will appear")
        print("  3. Open WhatsApp on your phone")
        print("  4. Settings → Linked Devices → Link a Device")
        print("  5. Scan the QR code")
        print("\nAfter authentication, run this test again to verify.")
        
    else:
        print("\n✓ WhatsApp is fully configured and ready!")
        print("\nStart WhatsApp watcher:")
        print("  → python main.py watcher-whatsapp")
        print("\nTest it:")
        print("  1. Send yourself a WhatsApp message with 'urgent'")
        print("  2. Wait up to 30 seconds")
        print("  3. Check AI_Employee_Vault/Needs_Action/ folder")
    
    print("\n" + "="*70)
    print("WhatsApp Test Complete")
    print("="*70)


if __name__ == "__main__":
    success = main()
    sys.exit(0)  # Always exit 0 - this is a check script
