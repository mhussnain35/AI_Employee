"""
Watcher module for AI Employee.

Watchers are lightweight Python scripts that run continuously,
monitoring various inputs and creating actionable files for Claude to process.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher scripts.
    
    All watchers follow this pattern:
    1. Check for updates from their data source
    2. Create action files in the Needs_Action folder
    3. Run continuously with a configurable check interval
    """
    
    def __init__(self, vault_path: str | Path, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        
        Returns:
            List of new items that need processing
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created action file
        """
        pass
    
    def run(self) -> None:
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        for item in items:
                            try:
                                filepath = self.create_action_file(item)
                                self.logger.info(f'Created action file: {filepath.name}')
                            except Exception as e:
                                self.logger.error(f'Error creating action file: {e}')
                    else:
                        self.logger.debug('No new items')
                except Exception as e:
                    self.logger.error(f'Error checking for updates: {e}')
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
    
    def update_dashboard(self, metric: str, value: str) -> None:
        """
        Update a metric in the Dashboard.md file.
        
        Args:
            metric: The metric name to update
            value: The new value for the metric
        """
        dashboard_path = self.vault_path / 'Dashboard.md'
        if not dashboard_path.exists():
            return
        
        content = dashboard_path.read_text()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Simple replacement - in production, use proper YAML parsing
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if metric.lower() in line.lower() and '|' in line:
                # Found the metric row, update it
                parts = line.split('|')
                if len(parts) >= 3:
                    parts[2] = f' {value} '
                    parts[3] = f' {timestamp} '
                    lines[i] = '|'.join(parts)
                    break
        
        dashboard_path.write_text('\n'.join(lines))
        self.logger.debug(f'Updated dashboard metric: {metric}')
