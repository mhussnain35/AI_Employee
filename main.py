#!/usr/bin/env python3
"""
AI Employee - Your Personal Digital FTE

A local-first, agent-driven digital FTE (Full-Time Equivalent) that
proactively manages your personal and business affairs 24/7.

Silver Tier Features:
- Obsidian vault with Dashboard and Company Handbook
- File System Watcher for monitoring drop folder
- Gmail Watcher for monitoring emails
- WhatsApp Watcher for monitoring messages
- Claude Code integration for processing tasks
- Basic folder structure: /Inbox, /Needs_Action, /Done
"""

import sys
import threading
import time
from pathlib import Path


def show_banner():
    """Display the AI Employee banner."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║           AI Employee - Your Digital FTE                 ║
║  Local-first, Agent-driven, Human-in-the-loop            ║
║                                                          ║
║  Tier: Silver (Gmail + WhatsApp + FileSystem)            ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def show_help():
    """Display help information."""
    help_text = """
AI Employee - Silver Tier

Usage:
    python main.py [command]

Commands:
    setup           Initialize the vault structure
    watcher         Start the file system watcher
    watcher-gmail   Start the Gmail watcher
    watcher-whatsapp Start the WhatsApp watcher
    watcher-all     Start all watchers (file, gmail, whatsapp)
    process         Process pending items in Needs_Action
    status          Show current vault status
    setup-gmail     Authenticate with Gmail API
    setup-whatsapp  Authenticate with WhatsApp Web
    help            Show this help message

Examples:
    python main.py setup              # Create vault folders
    python main.py setup-gmail        # Authenticate Gmail
    python main.py setup-whatsapp     # Authenticate WhatsApp
    python main.py watcher            # Start file watcher
    python main.py watcher-gmail      # Start Gmail watcher
    python main.py watcher-whatsapp   # Start WhatsApp watcher
    python main.py watcher-all        # Start all watchers
    python main.py process            # Process pending tasks

Quick Start:
    1. Setup authentication:
       - python main.py setup-gmail
       - python main.py setup-whatsapp
    
    2. Start watchers:
       - python main.py watcher-all
    
    3. Drop files in AI_Employee_Vault/Inbox/
    
    4. Process items:
       - python main.py process

For more information, see:
    - AI_Employee_Vault/README.md
    - AI_Employee_Vault/Company_Handbook.md
    - docs/GMAIL_SETUP.md
    - docs/WHATSAPP_SETUP.md
"""
    print(help_text)


def show_status(vault_path: Path):
    """Show the current vault status."""
    print("\n" + "=" * 60)
    print("AI Employee Vault Status")
    print("=" * 60)
    print(f"Vault Location: {vault_path}")
    
    if not vault_path.exists():
        print("\n✗ Vault does not exist. Run: python main.py setup")
        return
    
    # Count files in each folder
    folders = {
        'Inbox': 0,
        'Needs_Action': 0,
        'Done': 0,
        'Plans': 0,
        'Pending_Approval': 0,
    }
    
    for folder_name in folders:
        folder_path = vault_path / folder_name
        if folder_path.exists():
            count = len(list(folder_path.glob('*.md')))
            folders[folder_name] = count
    
    print("\nFolder Contents:")
    for folder, count in folders.items():
        print(f"  {folder:20s}: {count} file(s)")
    
    # Check key files
    print("\nKey Files:")
    key_files = ['Dashboard.md', 'Company_Handbook.md']
    for filename in key_files:
        filepath = vault_path / filename
        exists = "✓" if filepath.exists() else "✗"
        print(f"  {exists} {filename}")
    
    # Check credentials
    print("\nCredentials:")
    credentials_dir = Path(__file__).parent / 'credentials'
    creds_files = ['credentials.json', 'token.json']
    for filename in creds_files:
        filepath = credentials_dir / filename
        exists = "✓" if filepath.exists() else "✗"
        print(f"  {exists} {filename}")
    
    # Check sessions
    print("\nSessions:")
    sessions_dir = Path(__file__).parent / 'sessions'
    whatsapp_session = sessions_dir / 'whatsapp'
    exists = "✓" if whatsapp_session.exists() else "✗"
    print(f"  {exists} WhatsApp session")
    
    print("=" * 60)


def cmd_setup_gmail():
    """Run Gmail authentication."""
    from scripts.gmail_auth import main as gmail_auth_main
    gmail_auth_main()


def cmd_setup_whatsapp():
    """Run WhatsApp authentication."""
    from scripts.whatsapp_init import main as whatsapp_init_main
    whatsapp_init_main()


def cmd_watcher_gmail(vault_path: Path):
    """Start Gmail watcher."""
    from watchers import GmailWatcher
    
    print("\nStarting Gmail Watcher...")
    print("Press Ctrl+C to stop")
    print(f"Vault: {vault_path}")
    print("-" * 60)
    
    watcher = GmailWatcher(vault_path, check_interval=120)
    watcher.run()


def cmd_watcher_whatsapp(vault_path: Path):
    """Start WhatsApp watcher."""
    from watchers import WhatsAppWatcher
    
    print("\nStarting WhatsApp Watcher...")
    print("Press Ctrl+C to stop")
    print(f"Vault: {vault_path}")
    print("-" * 60)
    
    watcher = WhatsAppWatcher(vault_path, check_interval=30)
    watcher.run()


def cmd_watcher_all(vault_path: Path):
    """Start all watchers in parallel."""
    from watchers import FileSystemWatcher, GmailWatcher, WhatsAppWatcher
    
    print("\nStarting All Watchers...")
    print("Press Ctrl+C to stop")
    print(f"Vault: {vault_path}")
    print("-" * 60)
    
    # Create watchers
    fs_watcher = FileSystemWatcher(vault_path, check_interval=5)
    gmail_watcher = GmailWatcher(vault_path, check_interval=120)
    whatsapp_watcher = WhatsAppWatcher(vault_path, check_interval=30)
    
    # Start in separate threads
    threads = []
    
    print("\nStarting File System Watcher...")
    fs_thread = threading.Thread(target=fs_watcher.run, daemon=True)
    fs_thread.start()
    threads.append(fs_thread)
    
    print("Starting Gmail Watcher...")
    gmail_thread = threading.Thread(target=gmail_watcher.run, daemon=True)
    gmail_thread.start()
    threads.append(gmail_thread)
    
    print("Starting WhatsApp Watcher...")
    whatsapp_thread = threading.Thread(target=whatsapp_watcher.run, daemon=True)
    whatsapp_thread.start()
    threads.append(whatsapp_thread)
    
    print("\n✓ All watchers started")
    print("Monitoring for new items...")
    print("-" * 60)
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping all watchers...")


def main():
    """Main entry point for AI Employee."""
    show_banner()
    
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    if len(sys.argv) < 2:
        show_help()
        show_status(vault_path)
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        print("\nSetting up vault structure...")
        from setup_vault import setup_vault
        setup_vault(vault_path)
        print("\n✓ Setup complete!")

    elif command == "run":
        # Start the complete AI Employee system
        print("\n" + "="*70)
        print("Starting AI Employee System...")
        print("="*70)
        print("\nThis will start:")
        print("  • File System Watcher")
        print("  • Gmail Watcher (if authenticated)")
        print("  • WhatsApp Watcher (if authenticated)")
        print("  • Orchestrator")
        print("\n" + "="*70)
        
        # Import and run the system runner
        from run_system import main as run_system_main
        run_system_main()

    elif command == "watcher":
        print("\nStarting File System Watcher...")
        print("Press Ctrl+C to stop")
        print(f"Watching: {vault_path / 'Inbox'}")
        print("-" * 60)
        
        from watchers import FileSystemWatcher
        watcher = FileSystemWatcher(vault_path, check_interval=2)
        watcher.run()
        
    elif command == "watcher-gmail":
        cmd_watcher_gmail(vault_path)
        
    elif command == "watcher-whatsapp":
        cmd_watcher_whatsapp(vault_path)
        
    elif command == "watcher-all":
        cmd_watcher_all(vault_path)
        
    elif command == "process":
        print("\nProcessing pending items...")
        from orchestrator import Orchestrator
        orchestrator = Orchestrator(vault_path)
        orchestrator.run()
        
    elif command == "status":
        show_status(vault_path)
        
    elif command == "setup-gmail":
        cmd_setup_gmail()
        
    elif command == "setup-whatsapp":
        cmd_setup_whatsapp()
        
    elif command == "help":
        show_help()
        
    else:
        print(f"\n✗ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
