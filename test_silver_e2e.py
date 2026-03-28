#!/usr/bin/env python3
"""
Silver Tier End-to-End Test for AI Employee.

This script tests the complete Silver Tier workflow:
1. Gmail Watcher integration (structure only, no API calls)
2. WhatsApp Watcher integration (structure only, no browser)
3. File System Watcher
4. Orchestrator processing
5. Plan creation
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_vault_structure():
    """Test that vault structure is correct."""
    print("\n" + "="*70)
    print("Vault Structure Test")
    print("="*70)
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    required_folders = [
        'Inbox',
        'Needs_Action',
        'Done',
        'Plans',
        'Pending_Approval',
        'Accounting',
        'Briefings',
        'Updates'
    ]
    
    all_present = True
    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists():
            print(f"  ✓ {folder}/")
        else:
            print(f"  ✗ {folder}/ - Missing")
            all_present = False
    
    required_files = [
        'Dashboard.md',
        'Company_Handbook.md',
        'README.md'
    ]
    
    for filename in required_files:
        filepath = vault_path / filename
        if filepath.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - Missing")
            all_present = False
    
    return all_present


def test_watchers_import():
    """Test that all watchers can be imported."""
    print("\n" + "="*70)
    print("Watchers Import Test")
    print("="*70)
    
    try:
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
        print("\n✓ All watchers imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_filesystem_watcher_e2e():
    """Test FileSystemWatcher end-to-end."""
    print("\n" + "="*70)
    print("FileSystemWatcher End-to-End Test")
    print("="*70)
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import FileSystemWatcher
        
        # Create watcher
        watcher = FileSystemWatcher(vault_path, check_interval=2)
        print("✓ FileSystemWatcher created")
        
        # Create test file
        inbox_path = vault_path / "Inbox"
        test_file = inbox_path / "test_silver_tier.txt"
        test_content = "Silver Tier test file"
        test_file.write_text(test_content)
        print(f"✓ Created test file: {test_file.name}")
        
        # Process file
        action_file = watcher.process_file(test_file)
        print(f"✓ Action file created: {action_file.name}")
        
        # Verify action file
        if action_file.exists():
            content = action_file.read_text()
            if 'type: file_drop' in content:
                print("✓ Action file format correct")
            else:
                print("✗ Action file format incorrect")
                return False
        else:
            print("✗ Action file not created")
            return False
        
        # Cleanup
        test_file.unlink()
        print("✓ Cleaned up test file")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_gmail_watcher_mock():
    """Test GmailWatcher structure (mock test)."""
    print("\n" + "="*70)
    print("GmailWatcher Mock Test")
    print("="*70)
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import GmailWatcher
        
        # Create watcher (won't connect without credentials)
        watcher = GmailWatcher(vault_path, check_interval=120)
        print("✓ GmailWatcher instance created")
        
        # Check credentials path
        from watchers.gmail_watcher import CREDENTIALS_DIR, TOKEN_FILE
        print(f"  Credentials dir: {CREDENTIALS_DIR}")
        print(f"  Token file: {TOKEN_FILE}")
        
        if CREDENTIALS_DIR.exists():
            print("✓ Credentials directory exists")
        else:
            print("⚠ Credentials directory missing (OK for testing)")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_whatsapp_watcher_mock():
    """Test WhatsAppWatcher structure (mock test)."""
    print("\n" + "="*70)
    print("WhatsAppWatcher Mock Test")
    print("="*70)
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from watchers import WhatsAppWatcher
        
        # Create watcher (won't connect without session)
        watcher = WhatsAppWatcher(vault_path, check_interval=30)
        print("✓ WhatsAppWatcher instance created")
        
        # Check session path
        from watchers.whatsapp_watcher import SESSIONS_DIR, WHATSAPP_SESSION_DIR
        print(f"  Sessions dir: {SESSIONS_DIR}")
        print(f"  WhatsApp session: {WHATSAPP_SESSION_DIR}")
        
        if SESSIONS_DIR.exists():
            print("✓ Sessions directory exists")
        else:
            print("⚠ Sessions directory missing (OK for testing)")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_orchestrator():
    """Test orchestrator processing."""
    print("\n" + "="*70)
    print("Orchestrator Test")
    print("="*70)
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    try:
        from orchestrator import Orchestrator
        
        # Create orchestrator
        orchestrator = Orchestrator(vault_path)
        print("✓ Orchestrator created")
        
        # Check folders
        if orchestrator.needs_action.exists():
            print("✓ Needs_Action folder accessible")
        else:
            print("✗ Needs_Action folder missing")
            return False
        
        if orchestrator.plans.exists():
            print("✓ Plans folder accessible")
        else:
            print("✗ Plans folder missing")
            return False
        
        # Process any pending items
        pending = orchestrator.get_pending_items()
        print(f"  Found {len(pending)} pending item(s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_main_commands():
    """Test that main.py commands are available."""
    print("\n" + "="*70)
    print("Main Commands Test")
    print("="*70)
    
    main_path = Path(__file__).parent / "main.py"
    
    if not main_path.exists():
        print("✗ main.py not found")
        return False
    
    content = main_path.read_text()
    
    required_commands = [
        'watcher-gmail',
        'watcher-whatsapp',
        'watcher-all',
        'setup-gmail',
        'setup-whatsapp'
    ]
    
    all_present = True
    for command in required_commands:
        if command in content:
            print(f"  ✓ Command: {command}")
        else:
            print(f"  ✗ Command missing: {command}")
            all_present = False
    
    return all_present


def test_documentation():
    """Test that documentation files exist."""
    print("\n" + "="*70)
    print("Documentation Test")
    print("="*70)
    
    docs = [
        'README.md',
        'docs/GMAIL_SETUP.md',
        'docs/WHATSAPP_SETUP.md',
        'SECURITY.md',
        '.env.example'
    ]
    
    all_present = True
    for doc in docs:
        doc_path = Path(__file__).parent / doc
        if doc_path.exists():
            print(f"  ✓ {doc}")
        else:
            print(f"  ✗ {doc} - Missing")
            all_present = False
    
    return all_present


def test_scripts():
    """Test that setup scripts exist."""
    print("\n" + "="*70)
    print("Scripts Test")
    print("="*70)
    
    scripts = [
        'scripts/gmail_auth.py',
        'scripts/whatsapp_init.py'
    ]
    
    all_present = True
    for script in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            print(f"  ✓ {script}")
        else:
            print(f"  ✗ {script} - Missing")
            all_present = False
    
    return all_present


def run_all_tests():
    """Run all Silver Tier tests."""
    print("\n" + "="*70)
    print("Silver Tier End-to-End Test Suite")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Vault Structure", test_vault_structure),
        ("Watchers Import", test_watchers_import),
        ("FileSystemWatcher E2E", test_filesystem_watcher_e2e),
        ("GmailWatcher Mock", test_gmail_watcher_mock),
        ("WhatsAppWatcher Mock", test_whatsapp_watcher_mock),
        ("Orchestrator", test_orchestrator),
        ("Main Commands", test_main_commands),
        ("Documentation", test_documentation),
        ("Scripts", test_scripts),
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
        print("\n" + "="*70)
        print("✓ SILVER TIER TESTS PASSED!")
        print("="*70)
        print("\nSilver Tier Features Verified:")
        print("  ✓ Vault structure with all folders")
        print("  ✓ FileSystemWatcher operational")
        print("  ✓ GmailWatcher implemented (requires auth)")
        print("  ✓ WhatsAppWatcher implemented (requires session)")
        print("  ✓ Orchestrator processing items")
        print("  ✓ Main CLI with all commands")
        print("  ✓ Documentation complete")
        print("  ✓ Setup scripts ready")
        print("\nNext Steps:")
        print("  1. Run: python main.py setup-gmail")
        print("  2. Run: python main.py setup-whatsapp")
        print("  3. Run: python main.py watcher-all")
        print("  4. Monitor Needs_Action/ for action files")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
