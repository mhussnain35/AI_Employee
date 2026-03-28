"""
File System Watcher for AI Employee.

Monitors a drop folder for new files and creates action files
in the Needs_Action folder for Claude to process.
"""

import shutil
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handle file system events for the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        self.watcher = watcher
        self.logger = watcher.logger
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        source_path = Path(event.src_path)
        
        # Ignore temporary files
        if source_path.name.startswith('~') or source_path.suffix in ['.tmp', '.swp']:
            return
        
        self.logger.info(f'New file detected: {source_path.name}')
        
        try:
            self.watcher.process_file(source_path)
        except Exception as e:
            self.logger.error(f'Error processing file {source_path.name}: {e}')


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a file is created in the Inbox folder, it creates
    a corresponding action file in Needs_Action with metadata.
    """
    
    def __init__(self, vault_path: str | Path, check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 5 for file watcher)
        """
        super().__init__(vault_path, check_interval)
        self.drop_folder = self.inbox  # Files dropped in Inbox
        self.processed_files: set[str] = set()
        self.observer: Observer | None = None
    
    def start(self) -> None:
        """Start the file system observer."""
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        event_handler = DropFolderHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        self.observer.start()
        self.logger.info(f'Watching folder: {self.drop_folder}')
    
    def stop(self) -> None:
        """Stop the file system observer."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.info('File system watcher stopped')
    
    def process_file(self, source_path: Path) -> Path:
        """
        Process a new file and create an action file.
        
        Args:
            source_path: Path to the new file
            
        Returns:
            Path to the created action file
        """
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_filename = f'FILE_{timestamp}_{source_path.name}.md'
        action_path = self.needs_action / action_filename
        
        # Create metadata content
        content = f'''---
type: file_drop
original_name: {source_path.name}
size: {source_path.stat().st_size}
created: {datetime.now().isoformat()}
status: pending
---

# New File Dropped for Processing

**Original File:** `{source_path.name}`

**Size:** {source_path.stat().st_size} bytes

**Detected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Suggested Actions

- [ ] Review file content
- [ ] Categorize file
- [ ] Take required action
- [ ] Move to /Done when complete

'''
        
        action_path.write_text(content)
        self.logger.info(f'Created action file: {action_path.name}')
        
        return action_path
    
    def check_for_updates(self) -> list:
        """
        Check for new files in the drop folder.
        
        This method is called by the base run loop, but for the file watcher,
        we rely on the observer for real-time detection.
        
        Returns:
            Empty list (observer handles detection)
        """
        return []
    
    def create_action_file(self, item) -> Path:
        """
        Create an action file for an item.
        
        For file system watcher, this is handled by process_file().
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created action file
        """
        return self.process_file(item)
    
    def run(self) -> None:
        """
        Main run loop for the file system watcher.
        
        Uses the watchdog observer for real-time file monitoring.
        """
        self.start()
        
        try:
            while True:
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info('File system watcher stopped by user')
        finally:
            self.stop()


# Import time here to avoid circular dependency
import time
