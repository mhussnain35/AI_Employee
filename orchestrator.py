#!/usr/bin/env python3
"""
Orchestrator for AI Employee with AI Brain Integration.

This script processes files in the Needs_Action folder using the AI Brain
(Claude Code or Qwen API). It reads the Company Handbook for rules and
creates intelligent action plans.

Configuration:
    Set AI_BRAIN in .env file:
    - AI_BRAIN=claude  (uses Claude Code CLI)
    - AI_BRAIN=qwen    (uses Qwen API)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class Orchestrator:
    """Orchestrate AI-powered processing of action items."""
    
    def __init__(self, vault_path: str | Path, use_ai: bool = True):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            use_ai: Whether to use AI brain for processing (default: True)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.handbook = self.vault_path / 'Company_Handbook.md'
        self.use_ai = use_ai
        
        # Initialize AI brain if requested
        self.brain = None
        if use_ai:
            try:
                from ai_brain import AIBrain
                self.brain = AIBrain()
                print(f"✓ AI Brain initialized: {self.brain}")
            except Exception as e:
                print(f"⚠ Failed to initialize AI Brain: {e}")
                print("  Falling back to template-based processing")
                self.use_ai = False
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)
        self.plans.mkdir(parents=True, exist_ok=True)
    
    def get_pending_items(self) -> list[Path]:
        """Get all pending action files."""
        return sorted(self.needs_action.glob('*.md'))
    
    def process_item(self, item_path: Path) -> bool:
        """
        Process a single action item using AI Brain.
        
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
        
        # Read company handbook
        handbook_content = ""
        if self.handbook.exists():
            handbook_content = self.handbook.read_text()
            print(f"Company Handbook: Loaded ({len(handbook_content)} chars)")
        
        try:
            if self.use_ai and self.brain:
                # Use AI Brain for intelligent processing
                print(f"Using AI Brain ({self.brain.brain_type}) for reasoning...")
                
                # Classify the item
                print("  Classifying item...")
                classification = self.brain.classify_item(content)
                print(f"  Type: {classification.get('type', 'unknown')}")
                print(f"  Priority: {classification.get('priority', 'normal')}")
                
                # Create intelligent plan with AI
                print("  Creating action plan with AI...")
                plan_content = self.brain.create_plan(content, handbook_content, item_path)
                
                # Save the AI-generated plan
                plan_path = self._save_plan(plan_content, item_path, classification)
                print(f"✓ Created AI-generated plan: {plan_path.name}")
                
                # Move item to Done after processing
                print("  Moving item to Done folder...")
                self._move_to_done(item_path)
                print(f"✓ Item moved to Done/")
                
            else:
                # Fallback to template-based processing
                print("Using template-based processing (AI not available)...")
                plan_path = self._create_template_plan(item_path, content)
                print(f"✓ Created template plan: {plan_path.name}")
                
                # Move item to Done after processing
                print("  Moving item to Done folder...")
                self._move_to_done(item_path)
                print(f"✓ Item moved to Done/")
            
            return True
            
        except Exception as e:
            print(f"✗ Error processing item: {e}")
            print("  Falling back to template processing...")
            
            try:
                plan_path = self._create_template_plan(item_path, content)
                print(f"✓ Created fallback template plan: {plan_path.name}")
                
                # Move item to Done even on error
                print("  Moving item to Done folder...")
                self._move_to_done(item_path)
                print(f"✓ Item moved to Done/")
                return True
            except Exception as e2:
                print(f"✗ Fallback failed: {e2}")
                return False
    
    def _move_to_done(self, item_path: Path) -> Path:
        """
        Move an item from Needs_Action to Done folder.
        
        Args:
            item_path: Path to the item file
            
        Returns:
            Path to the file in Done folder
        """
        done_path = self.done / item_path.name
        
        # Add completion timestamp
        content = item_path.read_text()
        
        # Check if already has completion info
        if 'completed:' not in content.lower():
            # Add completion metadata
            if '---' in content:
                # Has frontmatter, add completed status
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    if 'completed:' not in frontmatter:
                        frontmatter += f"\ncompleted: {datetime.now().isoformat()}"
                        content = f"---{frontmatter}---{parts[2]}"
            
            # Add completion note at end
            content += f"\n\n---\n\n**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n*Processed by AI Employee Orchestrator*"
        
        # Write to Done folder
        done_path.write_text(content)
        
        # Remove from Needs_Action
        item_path.unlink()
        
        return done_path
    
    def _save_plan(self, plan_content: str, item_path: Path, 
                   classification: dict) -> Path:
        """Save AI-generated plan to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_name = f"PLAN_{timestamp}_{item_path.stem}.md"
        plan_path = self.plans / plan_name
        
        # Add frontmatter to plan
        full_content = f"""---
type: ai_plan
created: {datetime.now().isoformat()}
source_file: {item_path.name}
item_type: {classification.get('type', 'unknown')}
priority: {classification.get('priority', 'normal')}
ai_brain: {self.brain.brain_type if self.brain else 'none'}
status: pending
---

{plan_content}
"""
        
        plan_path.write_text(full_content)
        return plan_path
    
    def _create_template_plan(self, item_path: Path, content: str) -> Path:
        """Create a template plan (fallback when AI not available)."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_name = f"PLAN_{timestamp}_{item_path.stem}.md"
        plan_path = self.plans / plan_name
        
        # Extract type from content
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
{content[:1000]}
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
*This is a template plan. Configure AI_BRAIN in .env for intelligent processing.*

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
        print(f"AI Brain: {'Enabled' if self.use_ai and self.brain else 'Disabled'}")
        if self.brain:
            print(f"Brain Type: {self.brain.brain_type}")
        
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
    
    # Check if AI should be used
    use_ai = '--no-ai' not in sys.argv
    
    orchestrator = Orchestrator(vault_path, use_ai=use_ai)
    orchestrator.run()


if __name__ == "__main__":
    main()
