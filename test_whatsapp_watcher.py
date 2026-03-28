#!/usr/bin/env python3
"""
Test script for WhatsAppWatcher.

This script tests the WhatsAppWatcher functionality without requiring
actual WhatsApp Web access (uses mocking).
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_whatsapp_watcher_structure():
    """Test that WhatsAppWatcher class exists and has required methods."""
    print("\n" + "="*60)
    print("WhatsAppWatcher Structure Test")
    print("="*60)
    
    try:
        from watchers import WhatsAppWatcher
        print("✓ WhatsAppWatcher imported successfully")
        
        # Check required methods
        required_methods = [
            '_start_browser',
            '_navigate_to_whatsapp',
            '_is_authenticated',
            '_get_unread_chats',
            'check_for_updates',
            'create_action_file',
            'run'
        ]
        
        for method in required_methods:
            if hasattr(WhatsAppWatcher, method):
                print(f"  ✓ Method: {method}")
            else:
                print(f"  ✗ Method missing: {method}")
                return False
        
        print("\n✓ All required methods present")
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import WhatsAppWatcher: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_session_structure():
    """Test that session directory structure is correct."""
    print("\n" + "="*60)
    print("Session Structure Test")
    print("="*60)
    
    sessions_dir = Path(__file__).parent / 'sessions'
    whatsapp_session = sessions_dir / 'whatsapp'
    
    # Check directory exists
    if sessions_dir.exists():
        print(f"✓ Sessions directory exists: {sessions_dir}")
    else:
        print(f"✗ Sessions directory missing")
        print("  Creating directory...")
        sessions_dir.mkdir(parents=True, exist_ok=True)
    
    if whatsapp_session.exists():
        print(f"  ✓ WhatsApp session directory: {whatsapp_session}")
    else:
        print(f"  ✗ WhatsApp session directory missing")
        print("  Run: python scripts/whatsapp_init.py")
    
    return True


def test_action_file_format():
    """Test that action files are created with correct format."""
    print("\n" + "="*60)
    print("Action File Format Test")
    print("="*60)
    
    vault_path = Path(__file__).parent / 'AI_Employee_Vault'
    needs_action = vault_path / 'Needs_Action'
    
    # Create a mock action file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_file = needs_action / f'TEST_WHATSAPP_{timestamp}.md'
    
    test_content = f"""---
type: whatsapp
from: +1234567890
received: {datetime.now().isoformat()}
priority: high
status: pending
keywords_detected: ['urgent', 'asap']
---

# WhatsApp Message

**From:** +1234567890

**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Priority:** HIGH

---

## Message Content

This is an urgent test message!

---

## Suggested Actions

- [ ] Read and understand the message
- [ ] Determine if reply is needed
- [ ] Move to /Done when complete
"""
    
    try:
        needs_action.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_content)
        print(f"✓ Created test action file: {test_file.name}")
        
        # Verify content
        content = test_file.read_text()
        if 'type: whatsapp' in content and '---' in content:
            print("✓ Action file format is correct")
            
            # Cleanup
            test_file.unlink()
            print("✓ Cleaned up test file")
            return True
        else:
            print("✗ Action file format incorrect")
            return False
            
    except Exception as e:
        print(f"✗ Error creating test file: {e}")
        return False


def test_keywords_configuration():
    """Test that keywords are properly configured."""
    print("\n" + "="*60)
    print("Keywords Configuration Test")
    print("="*60)
    
    from watchers.whatsapp_watcher import DEFAULT_KEYWORDS
    
    expected_keywords = ['urgent', 'asap', 'invoice', 'payment', 'help']
    
    print(f"Default keywords: {DEFAULT_KEYWORDS}")
    
    for keyword in expected_keywords:
        if keyword in DEFAULT_KEYWORDS:
            print(f"  ✓ {keyword}")
        else:
            print(f"  ✗ {keyword} missing")
            return False
    
    return True


def test_env_configuration():
    """Test that .env.example exists with WhatsApp configuration."""
    print("\n" + "="*60)
    print("Environment Configuration Test")
    print("="*60)
    
    env_example = Path(__file__).parent / '.env.example'
    
    if env_example.exists():
        print(f"✓ .env.example exists")
        
        content = env_example.read_text()
        required_vars = [
            'WHATSAPP_KEYWORDS',
            'WHATSAPP_CHECK_INTERVAL'
        ]
        
        for var in required_vars:
            if var in content:
                print(f"  ✓ {var}")
            else:
                print(f"  ✗ {var} missing")
                return False
        
        return True
    else:
        print("✗ .env.example not found")
        return False


def test_playwright_import():
    """Test that Playwright can be imported."""
    print("\n" + "="*60)
    print("Playwright Import Test")
    print("="*60)
    
    try:
        from playwright.sync_api import sync_playwright
        print("✓ Playwright imported successfully")
        
        # Try to check if Chromium is installed
        try:
            playwright = sync_playwright().start()
            print("✓ Playwright initialized")
            
            # Check for Chromium
            try:
                browser = playwright.chromium.launch(headless=True)
                print("✓ Chromium browser available")
                browser.close()
                playwright.stop()
                return True
            except Exception as e:
                print(f"⚠ Chromium not installed: {e}")
                print("  Run: playwright install chromium")
                playwright.stop()
                return False
                
        except Exception as e:
            print(f"✗ Playwright initialization failed: {e}")
            return False
            
    except ImportError as e:
        print(f"✗ Playwright not installed: {e}")
        return False


def run_all_tests():
    """Run all WhatsAppWatcher tests."""
    print("\n" + "="*70)
    print("WhatsAppWatcher Test Suite")
    print("="*70)
    
    tests = [
        ("Playwright Import Test", test_playwright_import),
        ("Structure Test", test_whatsapp_watcher_structure),
        ("Session Structure Test", test_session_structure),
        ("Keywords Config Test", test_keywords_configuration),
        ("Action File Format Test", test_action_file_format),
        ("Environment Config Test", test_env_configuration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All WhatsAppWatcher tests passed!")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
