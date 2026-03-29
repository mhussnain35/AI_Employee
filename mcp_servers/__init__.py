"""MCP Servers for AI Employee.

This package provides Model Context Protocol (MCP) servers for:
- Gmail: Send emails, manage drafts
- WhatsApp: Send messages (future)
- Filesystem: Enhanced file operations (future)
"""

from .email_mcp import EmailMCPServer
from .whatsapp_mcp import WhatsAppMCPServer

__all__ = ['EmailMCPServer', 'WhatsAppMCPServer']
