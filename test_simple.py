#!/usr/bin/env python3
"""
Simple Test Script for Gmail and WhatsApp Watchers.

This script tests the structure and imports without requiring
actual API credentials or browser sessions.

Usage:
    python test_simple.py
"""

import sys
from pathlib import Path


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def test_imports():
    """Test that all modules can be imported."""
    print_header("Test 1: Module Imports")
    
    try:
        print("Importing watchers...")
        from watchers import (
            BaseWatcher,
            FileSystemWatcher,
            GmailWatcher,
            WhatsAppWatcher
        )
        print("  ✓ BaseWatcher")
        print("  ✓ FileSystemWatcher")
        print("  ✓ GmailWatcher")
        print("  ✓ WhatsAppWatcher")
        print("\n✓ All watchers imported successfully!")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        print("\n⚠ Dependencies not fully installed yet.")
        print("  Run: uv sync")
        print("  Run: playwright install chromium")
        return False


def test_filesystem_watcher():
    """Test FileSystemWatcher creates action files."""
    print_header("Test 2: FileSystemWatcher")
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import FileSystemWatcher
        
        # Create watcher
        watcher = FileSystemWatcher(vault_path, check_interval=2)
        print("  ✓ FileSystemWatcher created")
        
        # Create test file
        inbox = vault_path / "Inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        
        test_file = inbox / "simple_test.txt"
        test_file.write_text("Simple test content")
        print(f"  ✓ Created test file: {test_file.name}")
        
        # Process file
        action_file = watcher.process_file(test_file)
        print(f"  ✓ Action file created: {action_file.name}")
        
        # Verify content
        content = action_file.read_text()
        if "type: file_drop" in content:
            print("  ✓ Action file format correct")
        else:
            print("  ✗ Action file format incorrect")
            return False
        
        # Cleanup
        test_file.unlink()
        print("  ✓ Test file cleaned up")
        
        print("\n✓ FileSystemWatcher test PASSED!")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_gmail_structure():
    """Test GmailWatcher structure (without API)."""
    print_header("Test 3: GmailWatcher Structure")
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import GmailWatcher
        from watchers.gmail_watcher import CREDENTIALS_DIR, TOKEN_FILE
        
        # Create watcher instance
        watcher = GmailWatcher(vault_path, check_interval=120)
        print("  ✓ GmailWatcher instance created")
        
        # Check paths
        print(f"  Credentials directory: {CREDENTIALS_DIR}")
        print(f"  Token file: {TOKEN_FILE}")
        
        # Check if credentials exist
        creds_file = CREDENTIALS_DIR / "credentials.json"
        token_file = CREDENTIALS_DIR / "token.json"
        
        if creds_file.exists():
            print("  ✓ credentials.json found")
        else:
            print("  ⚠ credentials.json not found")
            print("    Run: python main.py setup-gmail")
        
        if token_file.exists():
            print("  ✓ token.json found (authenticated)")
        else:
            print("  ⚠ token.json not found")
            print("    Run: python main.py setup-gmail")
        
        # Check methods exist
        methods = [
            '_load_credentials',
            'check_for_updates',
            'create_action_file',
            '_get_message',
            'mark_as_read'
        ]
        
        for method in methods:
            if hasattr(watcher, method):
                print(f"  ✓ Method: {method}")
            else:
                print(f"  ✗ Method missing: {method}")
                return False
        
        print("\n✓ GmailWatcher structure test PASSED!")
        print("\nNext step: Run 'python main.py setup-gmail' to authenticate")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_whatsapp_structure():
    """Test WhatsAppWatcher structure (without browser)."""
    print_header("Test 4: WhatsAppWatcher Structure")
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import WhatsAppWatcher
        from watchers.whatsapp_watcher import SESSIONS_DIR, WHATSAPP_SESSION_DIR, DEFAULT_KEYWORDS
        
        # Create watcher instance
        watcher = WhatsAppWatcher(vault_path, check_interval=30)
        print("  ✓ WhatsAppWatcher instance created")
        
        # Check paths
        print(f"  Sessions directory: {SESSIONS_DIR}")
        print(f"  WhatsApp session: {WHATSAPP_SESSION_DIR}")
        
        # Check keywords
        print(f"  Monitored keywords: {DEFAULT_KEYWORDS}")
        
        # Check if session exists
        if WHATSAPP_SESSION_DIR.exists():
            print("  ✓ WhatsApp session folder found")
        else:
            print("  ⚠ WhatsApp session folder not found")
            print("    Run: python main.py setup-whatsapp")
        
        # Check methods exist
        methods = [
            '_start_browser',
            '_navigate_to_whatsapp',
            '_is_authenticated',
            '_get_unread_chats',
            'check_for_updates',
            'create_action_file'
        ]
        
        for method in methods:
            if hasattr(watcher, method):
                print(f"  ✓ Method: {method}")
            else:
                print(f"  ✗ Method missing: {method}")
                return False
        
        print("\n✓ WhatsAppWatcher structure test PASSED!")
        print("\nNext step: Run 'python main.py setup-whatsapp' to authenticate")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_main_commands():
    """Test that main.py has all required commands."""
    print_header("Test 5: Main CLI Commands")
    
    main_path = Path(__file__).parent / "main.py"
    
    if not main_path.exists():
        print("  ✗ main.py not found")
        return False
    
    content = main_path.read_text(encoding='utf-8')
    
    commands = [
        'watcher',
        'watcher-gmail',
        'watcher-whatsapp',
        'watcher-all',
        'setup-gmail',
        'setup-whatsapp',
        'process',
        'status'
    ]
    
    all_found = True
    for command in commands:
        if f'command == "{command}"' in content or f'"{command}"' in content:
            print(f"  ✓ Command: {command}")
        else:
            print(f"  ✗ Command missing: {command}")
            all_found = False
    
    if all_found:
        print("\n✓ All CLI commands present!")
        return True
    else:
        print("\n✗ Some commands missing")
        return False


def test_documentation():
    """Test that documentation files exist."""
    print_header("Test 6: Documentation")
    
    docs = {
        'README.md': 'Main documentation',
        'SECURITY.md': 'Security guide',
        'QUICKSTART_SILVER.md': 'Quick start guide',
        'SILVER_TIER_SUMMARY.md': 'Silver tier summary',
        'docs/GMAIL_SETUP.md': 'Gmail setup guide',
        'docs/WHATSAPP_SETUP.md': 'WhatsApp setup guide',
        '.env.example': 'Environment variables template'
    }
    
    all_exist = True
    for doc, description in docs.items():
        doc_path = Path(__file__).parent / doc
        if doc_path.exists():
            print(f"  ✓ {doc} - {description}")
        else:
            print(f"  ✗ {doc} - Missing")
            all_exist = False
    
    if all_exist:
        print("\n✓ All documentation present!")
        return True
    else:
        print("\n⚠ Some documentation missing")
        return False


def main():
    """Run all tests."""
    print_header("AI Employee - Simple Test Suite")
    print("Testing Gmail and WhatsApp Watchers")
    print_header("Running Tests...")
    
    tests = [
        ("Module Imports", test_imports),
        ("FileSystemWatcher", test_filesystem_watcher),
        ("GmailWatcher Structure", test_gmail_structure),
        ("WhatsAppWatcher Structure", test_whatsapp_structure),
        ("Main CLI Commands", test_main_commands),
        ("Documentation", test_documentation),
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
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*70)
        print("✓ ALL TESTS PASSED!")
        print("="*70)
        print("\nYour AI Employee Silver Tier is ready!")
        print("\nNext steps:")
        print("  1. python main.py setup-gmail     (authenticate Gmail)")
        print("  2. python main.py setup-whatsapp  (authenticate WhatsApp)")
        print("  3. python main.py watcher-all     (start all watchers)")
        print("="*70)
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        print("\nCheck the errors above and fix them before proceeding.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
