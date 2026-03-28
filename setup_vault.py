#!/usr/bin/env python3
"""Setup the Obsidian vault folder structure for AI Employee."""

from pathlib import Path


def setup_vault(vault_path: Path) -> None:
    """Create the folder structure for the AI Employee vault."""
    
    folders = [
        "Inbox",
        "Needs_Action",
        "Done",
        "Accounting",
        "Plans",
        "Pending_Approval",
        "Briefings",
        "Updates",
    ]
    
    for folder in folders:
        folder_path = vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {folder_path}")
    
    # Create .gitkeep files to ensure folders are tracked by git
    for folder in folders:
        folder_path = vault_path / folder
        gitkeep = folder_path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    
    print(f"\n✓ Vault structure created at: {vault_path}")


if __name__ == "__main__":
    # Default vault path - can be customized
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    setup_vault(vault_path)
