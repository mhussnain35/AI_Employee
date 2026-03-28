#!/usr/bin/env python3
"""
Orchestrator for AI Employee.

This script processes files in the Needs_Action folder using Claude Code.
It reads the Company Handbook for rules and creates action plans.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


class Orchestrator:
    """Orchestrate Claude Code processing of action items."""
    
    def __init__(self, vault_path: str | Path):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.handbook = self.vault_path / 'Company_Handbook.md'
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)
        self.plans.mkdir(parents=True, exist_ok=True)
    
    def get_pending_items(self) -> list[Path]:
        """Get all pending action files."""
        return sorted(self.needs_action.glob('*.md'))
    
    def process_item(self, item_path: Path) -> bool:
        """
        Process a single action item using Claude Code.
        
        Args:
            item_path: Path to the action file
            
        Returns:
            True if processed successfully, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Processing: {item_path.name}")
        print(f"{'='*60}")
        
        # Read the action file
        content = item_path.read_text()
        print(f"Content preview:\n{content[:200]}...\n")
        
        # Create a prompt for Claude Code
        prompt = self._create_prompt(item_path, content)
        
        # In Bronze Tier, we'll create a plan file instead of running Claude interactively
        # This demonstrates the workflow without requiring Claude Code subscription
        plan_path = self._create_plan(item_path, content)
        
        print(f"✓ Created plan: {plan_path.name}")
        print("Note: In production, Claude Code would process this interactively.")
        
        return True
    
    def _create_prompt(self, item_path: Path, content: str) -> str:
        """Create a prompt for Claude Code."""
        
        handbook_content = self.handbook.read_text() if self.handbook.exists() else ""
        
        prompt = f"""You are an AI Employee processing tasks from your Obsidian vault.

## Context
- Vault: {self.vault_path}
- Current Item: {item_path.name}
- Item Content:
{content}

## Company Handbook Rules
{handbook_content}

## Your Task
1. Read the item content above
2. Determine what action needs to be taken
3. Create a Plan.md file with checkboxes for each step
4. Follow the Company Handbook rules
5. Move the item to /Done when complete (or /Pending_Approval if approval needed)

## Output Format
For each action, create a checkbox:
- [ ] Action description

Be professional, efficient, and follow the handbook rules.
"""
        return prompt
    
    def _create_plan(self, item_path: Path, content: str) -> Path:
        """
        Create a plan file for the action item.
        
        In Bronze Tier, this demonstrates the workflow without
        requiring interactive Claude Code execution.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_name = f"PLAN_{timestamp}_{item_path.stem}.md"
        plan_path = self.plans / plan_name
        
        # Extract type from content if available
        item_type = "Unknown"
        for line in content.split('\n'):
            if line.startswith('type:'):
                item_type = line.split(':')[1].strip()
                break
        
        plan_content = f"""---
type: plan
created: {datetime.now().isoformat()}
source_file: {item_path.name}
item_type: {item_type}
status: pending
---

# Action Plan: {item_path.name}

## Source Content
```
{content}
```

## Required Actions

Based on the Company Handbook rules:

- [ ] Review the item content
- [ ] Determine priority level (Critical/High/Normal/Low)
- [ ] Identify required actions
- [ ] Execute actions (or request approval if needed)
- [ ] Update Dashboard.md with progress
- [ ] Move source file to /Done when complete

## Notes
*This plan was auto-generated. In production, Claude Code would fill in the specific actions.*

## Completion Checklist
- [ ] All actions completed
- [ ] Dashboard updated
- [ ] Source file moved to /Done
"""
        
        plan_path.write_text(plan_content)
        return plan_path
    
    def update_dashboard(self, pending_count: int, done_count: int) -> None:
        """Update the dashboard with current stats."""
        if not self.dashboard.exists():
            return
        
        content = self.dashboard.read_text()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Update pending tasks count
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Pending Tasks' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    parts[2] = f' {pending_count} '
                    parts[3] = f' {timestamp} '
                    lines[i] = '|'.join(parts)
        
        self.dashboard.write_text('\n'.join(lines))
    
    def run(self) -> None:
        """Process all pending items."""
        print("=" * 60)
        print("AI Employee Orchestrator")
        print("=" * 60)
        print(f"Vault: {self.vault_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        pending_items = self.get_pending_items()
        
        if not pending_items:
            print("\n✓ No pending items to process")
            self.update_dashboard(0, 0)
            return
        
        print(f"\nFound {len(pending_items)} pending item(s)")
        
        success_count = 0
        for item in pending_items:
            if self.process_item(item):
                success_count += 1
        
        # Update dashboard
        remaining = len(pending_items) - success_count
        self.update_dashboard(remaining, success_count)
        
        print(f"\n{'='*60}")
        print(f"Processing Complete: {success_count}/{len(pending_items)} items")
        print(f"{'='*60}")


def main():
    """Main entry point."""
    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault not found at {vault_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(vault_path)
    orchestrator.run()


if __name__ == "__main__":
    main()
