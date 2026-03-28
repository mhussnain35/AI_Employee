#!/usr/bin/env python3
"""
Gmail OAuth2 Authentication Script

This script helps you authenticate with the Gmail API and generate
a token.json file that will be used by the GmailWatcher.

Prerequisites:
1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Create OAuth2 credentials
4. Download credentials.json and place it in credentials/ folder

Usage:
    python scripts/gmail_auth.py
    or
    python main.py setup-gmail
"""

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import json
from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle


# Gmail API scopes - what permissions we need
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Paths
CREDENTIALS_DIR = Path(__file__).parent.parent / 'credentials'
CREDENTIALS_FILE = CREDENTIALS_DIR / 'credentials.json'
TOKEN_FILE = CREDENTIALS_DIR / 'token.json'


def setup_credentials_dir() -> None:
    """Create credentials directory if it doesn't exist."""
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Credentials directory: {CREDENTIALS_DIR}")


def check_credentials_file() -> bool:
    """Check if credentials.json exists and is valid."""
    if not CREDENTIALS_FILE.exists():
        print(f"\n✗ Error: credentials.json not found at {CREDENTIALS_FILE}")
        print("\nTo get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable 'Gmail API'")
        print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth client ID'")
        print("5. Choose 'Desktop app' as application type")
        print("6. Download the JSON file and save it as 'credentials.json' in credentials/ folder")
        return False
    
    # Validate JSON structure
    try:
        import json
        content = json.loads(CREDENTIALS_FILE.read_text())
        if 'installed' in content and 'client_id' in content['installed']:
            print(f"✓ Found valid credentials.json")
            print(f"  Project: {content['installed'].get('project_id', 'Unknown')}")
            print(f"  Client ID: {content['installed'].get('client_id', 'Unknown')[:50]}...")
            return True
        else:
            print(f"✗ Invalid credentials.json structure")
            return False
    except Exception as e:
        print(f"✗ Error reading credentials.json: {e}")
        return False


def authenticate() -> Optional[Credentials]:
    """
    Authenticate with Gmail API and return credentials.
    
    Returns:
        Credentials object if successful, None otherwise
    """
    creds = None

    # Load existing token if it exists
    if TOKEN_FILE.exists():
        print(f"✓ Found existing token.json")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"✗ Error loading token.json: {e}")
            print("  Token file may be corrupted, will create new one")
            creds = None
    
    # Check if we need to refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("✓ Token refreshed successfully")
            except Exception as e:
                print(f"✗ Token refresh failed: {e}")
                print("  Will re-authenticate")
                creds = None
        
        if not creds:
            print("\n" + "="*60)
            print("Starting Gmail OAuth2 Authentication")
            print("="*60)
            print("\nThis will open Chrome browser.")
            print("\nIMPORTANT: If you see 'This app isn't verified':")
            print("  1. Click 'Advanced'")
            print("  2. Click 'Go to AI Employee (unsafe)'")
            print("     (This is safe - it's your own app!)")
            print("  3. Click 'Allow' to grant permissions")
            print("\nStarting Chrome browser...")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                # Use Chrome browser specifically
                import webbrowser
                # Try to open Chrome specifically
                chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                try:
                    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab('about:blank')
                except:
                    pass  # Will use default browser if Chrome not found
                
                # Use port 8080 or the port from redirect_uris
                creds = flow.run_local_server(port=8080, open_browser=True, host='localhost')
                print("✓ Authentication successful!")
            except KeyboardInterrupt:
                print("\n\n✗ Authentication cancelled by user")
                return None
            except Exception as e:
                print(f"\n✗ Authentication failed: {e}")
                print("\nCommon issues:")
                print("  1. Port 8080 is blocked - try running as administrator")
                print("  2. Browser didn't open - check popup blocker")
                print("  3. Invalid credentials.json - verify file format")
                print("\nTry again: python main.py setup-gmail")
                return None
    
    # Save the credentials for next time
    if creds and creds.valid:
        print(f"\nSaving token to {TOKEN_FILE}...")
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print("✓ Token saved successfully")
            print("\n" + "="*60)
            print("Gmail Authentication Complete!")
            print("="*60)
            print(f"\nToken file: {TOKEN_FILE}")
            print("This token will be used automatically by GmailWatcher.")
            print("Token will auto-refresh when expired.")
            print("\nNext step: python main.py watcher-gmail")
            return creds
        except Exception as e:
            print(f"✗ Error saving token: {e}")
            print("\nAuthentication succeeded but token save failed.")
            print("You may need to authenticate again next time.")
            return creds  # Return creds anyway so watcher can work
    
    return None


def test_gmail_access(creds: Credentials) -> bool:
    """Test that we can access Gmail API."""
    try:
        from googleapiclient.discovery import build
        
        print("\nTesting Gmail API access...")
        service = build('gmail', 'v1', credentials=creds)
        
        # Get profile to test access
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress')
        
        print(f"✓ Successfully connected to Gmail!")
        print(f"  Account: {email}")
        return True
    except Exception as e:
        print(f"✗ Gmail API test failed: {e}")
        return False


def main():
    """Main entry point."""
    print("="*60)
    print("Gmail OAuth2 Authentication")
    print("="*60)
    
    # Setup
    setup_credentials_dir()
    
    if not check_credentials_file():
        print("\nExiting. Please add credentials.json and run again.")
        sys.exit(1)
    
    # Authenticate
    creds = authenticate()
    
    if not creds:
        print("\n✗ Authentication failed.")
        sys.exit(1)
    
    # Test access
    if not test_gmail_access(creds):
        print("\n⚠ Authentication succeeded but API test failed.")
        print("You may still try running the GmailWatcher.")
        sys.exit(1)
    
    print("\n✓ All checks passed! You can now use GmailWatcher.")
    print("\nNext steps:")
    print("1. Run: python main.py watcher-gmail")
    print("2. Or run: python main.py watcher-all (all watchers)")


if __name__ == "__main__":
    main()
