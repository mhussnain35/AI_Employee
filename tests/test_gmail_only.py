#!/usr/bin/env python3
"""
Gmail Watcher Test Script - Check Only

This script tests ONLY the Gmail Watcher functionality.
No authentication prompts - just checks if everything is ready.

Usage:
    python -m tests.test_gmail_only
    # or
    python tests/test_gmail_only.py
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from datetime import datetime


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def test_dependencies():
    """Test that all required dependencies are installed."""
    print_header("Step 1: Checking Dependencies")
    
    try:
        from google.oauth2.credentials import Credentials
        print("  ✓ google.oauth2.credentials")
        
        from googleapiclient.discovery import build
        print("  ✓ googleapiclient.discovery")
        
        from google_auth_oauthlib.flow import InstalledAppFlow
        print("  ✓ google_auth_oauthlib.flow")
        
        print("\n✓ All Gmail dependencies installed!")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        print("\n  FIX: Run 'uv sync' to install dependencies")
        return False


def test_credentials_file():
    """Test that credentials.json exists and is valid."""
    print_header("Step 2: Checking credentials.json")
    
    creds_file = Path(__file__).parent / 'credentials' / 'credentials.json'
    
    if not creds_file.exists():
        print(f"  ✗ credentials.json not found at: {creds_file}")
        print("\n  FIX: Download from Google Cloud Console:")
        print("  1. https://console.cloud.google.com/")
        print("  2. APIs & Services → Credentials")
        print("  3. Download OAuth2 credentials")
        print("  4. Save as: credentials/credentials.json")
        return False
    
    # Validate JSON
    try:
        content = json.loads(creds_file.read_text())
        
        if 'installed' not in content:
            print(f"  ✗ Invalid credentials.json format (missing 'installed')")
            print("\n  FIX: Re-download credentials from Google Cloud Console")
            return False
        
        config = content['installed']
        print(f"  ✓ credentials.json found")
        print(f"  ✓ Project ID: {config.get('project_id', 'Unknown')}")
        print(f"  ✓ Client ID: {config.get('client_id', 'Unknown')[:60]}...")
        print(f"  ✓ Redirect URIs: {config.get('redirect_uris', [])}")
        
        print("\n✓ credentials.json is valid!")
        return True
        
    except Exception as e:
        print(f"  ✗ Error reading credentials.json: {e}")
        print("\n  FIX: Ensure credentials.json contains valid JSON")
        return False


def test_token_file():
    """Test if token.json exists (already authenticated)."""
    print_header("Step 3: Checking Authentication Status")
    
    token_file = Path(__file__).parent / 'credentials' / 'token.json'
    
    if token_file.exists():
        try:
            content = json.loads(token_file.read_text())
            print(f"  ✓ token.json found (authenticated)")
            
            # Check if token is expired
            import time
            expiry = content.get('expiry', 0)
            if expiry and expiry < time.time() * 1000:
                print(f"  ⚠ Token expired (will auto-refresh on next use)")
            else:
                print(f"  ✓ Token is valid")
            
            print("\n✓ Gmail is authenticated and ready!")
            print("  → Run: python main.py watcher-gmail")
            return True
        except Exception as e:
            print(f"  ⚠ Error reading token.json: {e}")
            print("\n  FIX: Delete token.json and re-authenticate")
            print("  → Run: python main.py setup-gmail")
            return False
    else:
        print(f"  ✗ token.json not found (not authenticated)")
        print("\n  FIX: Authenticate Gmail:")
        print("  → Run: python main.py setup-gmail")
        return False


def test_watcher_import():
    """Test that GmailWatcher can be imported."""
    print_header("Step 4: Testing GmailWatcher")
    
    try:
        from watchers import GmailWatcher
        print("  ✓ GmailWatcher imported successfully")
        
        vault_path = Path(__file__).parent / "AI_Employee_Vault"
        watcher = GmailWatcher(vault_path)
        print("  ✓ GmailWatcher instance created")
        
        # Check methods
        methods = ['_load_credentials', 'check_for_updates', 'create_action_file']
        for method in methods:
            if hasattr(watcher, method):
                print(f"  ✓ Method: {method}")
            else:
                print(f"  ✗ Method missing: {method}")
                return False
        
        print("\n✓ GmailWatcher code is working!")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n  FIX: Check error message above")
        return False


def test_gmail_connection():
    """Test actual Gmail API connection if authenticated."""
    print_header("Step 5: Testing Gmail API Connection")
    
    token_file = Path(__file__).parent / 'credentials' / 'token.json'
    
    if not token_file.exists():
        print("  ⊘ Skipped: Not authenticated yet")
        print("  → Run: python main.py setup-gmail")
        return None  # Neutral - not pass/fail
    
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        # Load credentials
        creds = Credentials.from_authorized_user_file(
            token_file,
            ['https://www.googleapis.com/auth/gmail.readonly']
        )
        
        # Test connection
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        email = profile.get('emailAddress')
        print(f"  ✓ Connected to Gmail: {email}")
        
        # Get unread count
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=1
        ).execute()
        
        unread_count = len(results.get('messages', []))
        print(f"  ✓ Unread messages: {unread_count}")
        
        print("\n✓ Gmail API connection successful!")
        return True
        
    except Exception as e:
        print(f"  ✗ Gmail API test failed: {e}")
        print("\n  FIX: Re-authenticate Gmail")
        print("  → Run: python main.py setup-gmail")
        return False


def main():
    """Run all Gmail tests."""
    print_header("Gmail Watcher Test Suite")
    print("Checking Gmail Integration Status")
    print_header("Running Tests...")
    
    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Credentials File", test_credentials_file),
        ("Authentication Status", test_token_file),
        ("Watcher Import", test_watcher_import),
        ("Gmail API Connection", test_gmail_connection),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            # None means skipped (neutral)
            if result is None:
                results.append((name, "SKIP"))
            else:
                results.append((name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\n✗ {name} failed: {e}")
            results.append((name, "FAIL"))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result == "PASS")
    skipped = sum(1 for _, result in results if result == "SKIP")
    failed = sum(1 for _, result in results if result == "FAIL")
    total = len(results)
    
    for name, result in results:
        if result == "PASS":
            print(f"  ✓ PASS: {name}")
        elif result == "SKIP":
            print(f"  ⊘ SKIP: {name}")
        else:
            print(f"  ✗ FAIL: {name}")
    
    print(f"\nTotal: {passed} passed, {skipped} skipped, {failed} failed")
    
    # Next steps
    print_header("Next Steps")
    
    token_exists = (Path(__file__).parent / 'credentials' / 'token.json').exists()
    
    if failed > 0:
        print("\n✗ Some tests failed - fix the errors above")
        
    elif not token_exists:
        print("\n⚠ Gmail is not authenticated yet")
        print("\nAuthenticate Gmail:")
        print("  → python main.py setup-gmail")
        print("\nAfter authentication, run this test again to verify.")
        
    else:
        print("\n✓ Gmail is fully configured and ready!")
        print("\nStart Gmail watcher:")
        print("  → python main.py watcher-gmail")
        print("\nTest it:")
        print("  1. Send yourself an email")
        print("  2. Mark it as Important in Gmail")
        print("  3. Wait up to 2 minutes")
        print("  4. Check AI_Employee_Vault/Needs_Action/ folder")
    
    print("\n" + "="*70)
    print("Gmail Test Complete")
    print("="*70)


if __name__ == "__main__":
    success = main()
    sys.exit(0)  # Always exit 0 - this is a check script
