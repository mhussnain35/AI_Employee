"""Watchers module for AI Employee."""

from .base_watcher import BaseWatcher
from .filesystem_watcher import FileSystemWatcher
from .gmail_watcher import GmailWatcher
from .whatsapp_watcher import WhatsAppWatcher

__all__ = ['BaseWatcher', 'FileSystemWatcher', 'GmailWatcher', 'WhatsAppWatcher']
