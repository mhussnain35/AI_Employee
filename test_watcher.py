#!/usr/bin/env python3
"""
Test script for FileSystemWatcher.

This script:
1. Starts the FileSystemWatcher
2. Creates a test file in the Inbox folder
3. Verifies that an action file is created in Needs_Action
"""

import time
import threading
from pathlib import Path
from watchers import FileSystemWatcher


def test_filesystem_watcher():
    """Test the FileSystemWatcher functionality."""
    
    # Setup paths
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    vault_path.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("FileSystemWatcher Test")
    print("=" * 60)
    print(f"Vault Path: {vault_path}")
    
    # Create watcher
    watcher = FileSystemWatcher(vault_path, check_interval=2)
    
    # Start watcher in a separate thread
    watcher_thread = threading.Thread(target=watcher.run, daemon=True)
    watcher_thread.start()
    
    print("\n✓ Watcher started")
    print("Waiting for watcher to initialize...")
    time.sleep(2)
    
    # Create a test file in the Inbox folder
    inbox_path = vault_path / "Inbox"
    test_file = inbox_path / "test_document.txt"
    
    print(f"\n✓ Creating test file: {test_file}")
    test_file.write_text("This is a test document for the AI Employee to process.")
    
    # Wait for the watcher to detect and process the file
    print("Waiting for watcher to detect the file...")
    time.sleep(5)
    
    # Check if action file was created
    needs_action_path = vault_path / "Needs_Action"
    action_files = list(needs_action_path.glob("FILE_*.md"))
    
    if action_files:
        print(f"\n✓ SUCCESS: Action file created!")
        print(f"  Action file: {action_files[0].name}")
        
        # Display the content of the action file
        print("\n--- Action File Content ---")
        print(action_files[0].read_text())
        print("--- End of Content ---\n")
        
        # Cleanup test file
        test_file.unlink()
        print(f"✓ Cleaned up test file: {test_file.name}")
        
    else:
        print("\n✗ FAILED: No action file created")
        print(f"  Checked folder: {needs_action_path}")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    test_filesystem_watcher()
