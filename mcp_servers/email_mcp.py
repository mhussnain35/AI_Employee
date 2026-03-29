#!/usr/bin/env python3
"""
Email MCP Server for AI Employee

This MCP server provides email capabilities for the AI Employee system.
It allows Claude Code to send emails, create drafts, and manage Gmail.

Features:
- Send emails via Gmail API
- Create drafts
- Search emails
- Mark as read/unread

Usage:
    python -m mcp_servers.email_mcp
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class EmailMCPServer:
    """
    MCP Server for Email operations.
    
    Provides tools for:
    - Sending emails
    - Creating drafts
    - Searching emails
    - Managing labels
    """
    
    def __init__(self, vault_path: Optional[Path] = None):
        """
        Initialize the Email MCP server.
        
        Args:
            vault_path: Path to the Obsidian vault (optional)
        """
        self.vault_path = vault_path or Path(__file__).parent.parent / "AI_Employee_Vault"
        self.service = None
        
        # Initialize Gmail service
        self._init_gmail_service()
        
        logger.info(f"Email MCP Server initialized")
    
    def _init_gmail_service(self):
        """Initialize Gmail API service."""
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Load credentials
            token_file = Path(__file__).parent.parent / "credentials" / "token.json"
            
            if not token_file.exists():
                logger.warning("Gmail token not found. Email MCP will not be available.")
                logger.warning("Run: python main.py setup-gmail")
                return
            
            creds = Credentials.from_authorized_user_file(
                token_file,
                ['https://www.googleapis.com/auth/gmail.send',
                 'https://www.googleapis.com/auth/gmail.draft',
                 'https://www.googleapis.com/auth/gmail.readonly']
            )
            
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {e}")
    
    def send_email(self, to: str, subject: str, body: str, 
                   cc: Optional[str] = None, 
                   is_draft: bool = False) -> dict:
        """
        Send an email (or create draft).
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            cc: CC recipient (optional)
            is_draft: If True, create draft instead of sending
            
        Returns:
            dict with message_id and status
        """
        if not self.service:
            return {
                'success': False,
                'error': 'Gmail service not initialized. Run: python main.py setup-gmail'
            }
        
        try:
            from email.mime.text import MIMEText
            import base64
            
            # Create message
            message = MIMEText(body, 'plain')
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            if is_draft:
                # Create draft
                draft = self.service.users().drafts().create(
                    userId='me',
                    body={'message': {'raw': raw_message}}
                ).execute()
                
                logger.info(f"Draft created: {draft['id']}")
                return {
                    'success': True,
                    'message_id': draft['id'],
                    'draft_id': draft['id'],
                    'status': 'draft_created'
                }
            else:
                # Send email
                sent_message = self.service.users().messages().send(
                    userId='me',
                    body={'raw': raw_message}
                ).execute()
                
                logger.info(f"Email sent: {sent_message['id']}")
                return {
                    'success': True,
                    'message_id': sent_message['id'],
                    'thread_id': sent_message.get('threadId'),
                    'status': 'sent'
                }
                
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_emails(self, query: str, max_results: int = 10) -> list:
        """
        Search emails in Gmail.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results
            
        Returns:
            List of email summaries
        """
        if not self.service:
            return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_summaries = []
            
            for msg in messages:
                msg_detail = self.service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                
                headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
                
                email_summaries.append({
                    'id': msg['id'],
                    'from': headers.get('From', ''),
                    'to': headers.get('To', ''),
                    'subject': headers.get('Subject', ''),
                    'date': headers.get('Date', ''),
                    'snippet': msg_detail.get('snippet', '')
                })
            
            return email_summaries
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark an email as read.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful
        """
        if not self.service:
            return False
        
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            logger.info(f"Marked {message_id} as read")
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark as read: {e}")
            return False
    
    def get_tools(self) -> list:
        """
        Get list of available MCP tools.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                'name': 'send_email',
                'description': 'Send an email via Gmail',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'to': {'type': 'string', 'description': 'Recipient email'},
                        'subject': {'type': 'string', 'description': 'Email subject'},
                        'body': {'type': 'string', 'description': 'Email body'},
                        'cc': {'type': 'string', 'description': 'CC recipient'},
                        'is_draft': {'type': 'boolean', 'description': 'Create draft instead of sending'}
                    },
                    'required': ['to', 'subject', 'body']
                }
            },
            {
                'name': 'search_emails',
                'description': 'Search emails in Gmail',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'query': {'type': 'string', 'description': 'Gmail search query'},
                        'max_results': {'type': 'integer', 'description': 'Max results'}
                    },
                    'required': ['query']
                }
            },
            {
                'name': 'mark_email_read',
                'description': 'Mark an email as read',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'message_id': {'type': 'string', 'description': 'Gmail message ID'}
                    },
                    'required': ['message_id']
                }
            }
        ]
    
    def call_tool(self, name: str, args: dict) -> dict:
        """
        Call an MCP tool by name.
        
        Args:
            name: Tool name
            args: Tool arguments
            
        Returns:
            Tool result
        """
        if name == 'send_email':
            return self.send_email(
                to=args.get('to'),
                subject=args.get('subject'),
                body=args.get('body'),
                cc=args.get('cc'),
                is_draft=args.get('is_draft', False)
            )
        elif name == 'search_emails':
            return {
                'success': True,
                'emails': self.search_emails(
                    query=args.get('query'),
                    max_results=args.get('max_results', 10)
                )
            }
        elif name == 'mark_email_read':
            success = self.mark_as_read(args.get('message_id'))
            return {'success': success}
        else:
            return {
                'success': False,
                'error': f'Unknown tool: {name}'
            }


# MCP Server entry point for stdio transport
def run_stdio_server():
    """Run the MCP server with stdio transport."""
    import json
    
    server = EmailMCPServer()
    
    logger.info("Starting Email MCP Server (stdio mode)")
    
    # Read requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            
            # Handle initialize
            if request.get('method') == 'initialize':
                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {}
                        },
                        'serverInfo': {
                            'name': 'email-mcp',
                            'version': '1.0.0'
                        }
                    }
                }
            
            # Handle tools/list
            elif request.get('method') == 'tools/list':
                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {
                        'tools': server.get_tools()
                    }
                }
            
            # Handle tools/call
            elif request.get('method') == 'tools/call':
                tool_name = request.get('params', {}).get('name')
                tool_args = request.get('params', {}).get('arguments', {})
                
                result = server.call_tool(tool_name, tool_args)
                
                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'result': {
                        'content': [
                            {
                                'type': 'text',
                                'text': json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            else:
                response = {
                    'jsonrpc': '2.0',
                    'id': request.get('id'),
                    'error': {
                        'code': -32601,
                        'message': 'Method not found'
                    }
                }
            
            # Write response to stdout
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            error_response = {
                'jsonrpc': '2.0',
                'id': request.get('id') if 'request' in dir() else None,
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--stdio':
        run_stdio_server()
    else:
        # Test mode
        print("Email MCP Server Test")
        print("="*50)
        
        server = EmailMCPServer()
        print(f"✓ Server initialized")
        print(f"  Tools: {[t['name'] for t in server.get_tools()]}")
        
        if server.service:
            print("\n✓ Gmail service is available")
            print("\nTest search:")
            emails = server.search_emails('is:unread', max_results=3)
            for email in emails:
                print(f"  - {email['subject']}")
        else:
            print("\n⚠ Gmail service not available")
            print("  Run: python main.py setup-gmail")
