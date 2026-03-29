#!/usr/bin/env python3
"""
AI Brain - Main AI Processor for AI Employee

This module provides the "Brain" functionality for the AI Employee system.
It supports multiple AI backends (Claude Code, Qwen) and handles all reasoning tasks.

Configuration is done via .env file:
    AI_BRAIN=claude  # or "qwen"

Usage:
    from ai_brain import AIBrain
    
    brain = AIBrain()
    response = brain.process("What tasks need attention?")
"""

import os
import sys
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


class AIBrain:
    """
    Main AI Brain for the AI Employee system.
    
    Supports multiple AI backends:
    - Claude Code (CLI-based)
    - Qwen (API-based)
    
    The brain is responsible for:
    - Reasoning about tasks
    - Creating action plans
    - Following company handbook rules
    - Making decisions based on context
    """
    
    def __init__(self, brain_type: Optional[str] = None, use_mcp: bool = True):
        """
        Initialize the AI Brain.

        Args:
            brain_type: Type of AI brain to use ('claude' or 'qwen')
                       If None, reads from AI_BRAIN environment variable
            use_mcp: Whether to use MCP servers (default: True)
        """
        # Determine brain type
        if brain_type:
            self.brain_type = brain_type.lower()
        else:
            self.brain_type = os.getenv('AI_BRAIN', 'claude').lower()

        logger.info(f"Initializing AI Brain: {self.brain_type}")

        # Initialize the appropriate processor
        self.processor = self._initialize_processor()

        if not self.processor:
            raise ValueError(f"Failed to initialize AI brain: {self.brain_type}")

        # Initialize MCP servers if requested
        self.mcp_servers = {}
        if use_mcp:
            self._initialize_mcp_servers()

        logger.info(f"AI Brain '{self.brain_type}' initialized successfully")
        if self.mcp_servers:
            logger.info(f"MCP servers available: {list(self.mcp_servers.keys())}")
    
    def _initialize_processor(self):
        """Initialize the appropriate AI processor based on configuration."""

        if self.brain_type == 'claude':
            try:
                from claude_processor import ClaudeProcessor
                logger.info("Using Claude Code as AI brain")
                return ClaudeProcessor()
            except ImportError as e:
                logger.error(f"Failed to import Claude processor: {e}")
                logger.error("Make sure claude_processor.py exists and dependencies are installed")
                return None
            except Exception as e:
                logger.error(f"Failed to initialize Claude processor: {e}")
                return None

        elif self.brain_type == 'qwen':
            try:
                from qwen_processor import QwenProcessor
                logger.info("Using Qwen API as AI brain")
                return QwenProcessor()
            except ImportError as e:
                logger.error(f"Failed to import Qwen processor: {e}")
                logger.error("Make sure qwen_processor.py exists and dependencies are installed")
                return None
            except Exception as e:
                logger.error(f"Failed to initialize Qwen processor: {e}")
                return None

        else:
            logger.error(f"Unknown AI brain type: {self.brain_type}")
            logger.error("Supported types: 'claude', 'qwen'")
            return None
    
    def _initialize_mcp_servers(self):
        """Initialize MCP servers for external actions."""
        try:
            from mcp_servers import EmailMCPServer, WhatsAppMCPServer
            
            # Initialize Email MCP
            try:
                email_server = EmailMCPServer()
                if email_server.service:
                    self.mcp_servers['email'] = email_server
                    logger.info("Email MCP server initialized")
                else:
                    logger.warning("Email MCP server not available (Gmail not authenticated)")
            except Exception as e:
                logger.warning(f"Failed to initialize Email MCP: {e}")
            
            # Initialize WhatsApp MCP (stub)
            try:
                whatsapp_server = WhatsAppMCPServer()
                self.mcp_servers['whatsapp'] = whatsapp_server
                logger.info("WhatsApp MCP server initialized (stub)")
            except Exception as e:
                logger.warning(f"Failed to initialize WhatsApp MCP: {e}")
            
        except ImportError:
            logger.warning("MCP servers not available (mcp_servers package not found)")
        except Exception as e:
            logger.warning(f"Failed to initialize MCP servers: {e}")
    
    def use_mcp_tool(self, server_name: str, tool_name: str, args: dict) -> dict:
        """
        Use an MCP tool from a specific server.
        
        Args:
            server_name: Name of MCP server ('email', 'whatsapp', etc.)
            tool_name: Name of tool to call
            args: Tool arguments
            
        Returns:
            Tool result dictionary
        """
        if server_name not in self.mcp_servers:
            return {
                'success': False,
                'error': f'MCP server "{server_name}" not available'
            }
        
        server = self.mcp_servers[server_name]
        return server.call_tool(tool_name, args)
    
    def get_mcp_tools(self) -> dict:
        """
        Get all available MCP tools from all servers.
        
        Returns:
            Dictionary mapping server names to their tools
        """
        result = {}
        for name, server in self.mcp_servers.items():
            result[name] = server.get_tools()
        return result
    
    def process(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Process a prompt with the AI brain.
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary with additional information
            
        Returns:
            AI response as string
            
        Raises:
            RuntimeError: If processor is not initialized
        """
        if not self.processor:
            raise RuntimeError("AI Brain processor not initialized")
        
        logger.info(f"Processing prompt with {self.brain_type}...")
        
        try:
            response = self.processor.process(prompt, context)
            logger.info(f"Processing complete ({len(response)} characters)")
            return response
        except Exception as e:
            logger.error(f"Error processing prompt: {e}")
            raise
    
    def create_plan(self, item_content: str, handbook_content: str, 
                   item_path: Path) -> str:
        """
        Create an action plan for an item using AI reasoning.
        
        Args:
            item_content: Content of the item to process
            handbook_content: Company handbook rules
            item_path: Path to the item file
            
        Returns:
            Generated plan as markdown string
        """
        prompt = f"""You are an AI Employee processing tasks from your Obsidian vault.

## Context
- Current Item: {item_path.name}
- Vault Path: {item_path.parent}

## Company Handbook Rules
{handbook_content}

## Item to Process
{item_content}

## Your Task
Analyze this item and create a detailed action plan following the Company Handbook rules.

Your plan should include:
1. Priority level (Critical/High/Normal/Low)
2. Specific actions required (as checkboxes)
3. Any approvals needed (for payments > $500, sensitive actions)
4. Expected outcome

## Output Format
Respond with a markdown-formatted plan including:
- Priority assessment
- Action items as checkboxes (- [ ])
- Any required approvals
- Notes or considerations

Be professional, efficient, and follow the handbook rules."""

        context = {
            'item_path': str(item_path),
            'handbook_path': str(item_path.parent.parent / 'Company_Handbook.md')
        }
        
        return self.process(prompt, context)
    
    def classify_item(self, item_content: str) -> dict:
        """
        Classify an item to determine its type and priority.
        
        Args:
            item_content: Content of the item
            
        Returns:
            Dictionary with classification results
        """
        prompt = f"""Analyze this item and classify it:

{item_content}

Respond with a JSON object containing:
{{
    "type": "email|whatsapp|file_drop|other",
    "priority": "critical|high|normal|low",
    "requires_approval": true|false,
    "category": "communication|finance|task|other",
    "keywords": ["keyword1", "keyword2"]
}}

Only respond with the JSON object, no other text."""

        response = self.process(prompt)
        
        # Parse JSON response
        import json
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning("No JSON found in response")
                return self._default_classification()
        except Exception as e:
            logger.error(f"Failed to parse classification: {e}")
            return self._default_classification()
    
    def _default_classification(self) -> dict:
        """Return default classification if AI fails."""
        return {
            'type': 'other',
            'priority': 'normal',
            'requires_approval': False,
            'category': 'other',
            'keywords': []
        }
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Summarize a text using AI.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary string
        """
        prompt = f"""Summarize the following text in {max_length} characters or less:

{text}

Provide a concise summary that captures the key points."""

        return self.process(prompt)
    
    def extract_action_items(self, text: str) -> list:
        """
        Extract action items from text.
        
        Args:
            text: Text to extract action items from
            
        Returns:
            List of action items
        """
        prompt = f"""Extract all action items from this text:

{text}

Respond with a JSON array of action items:
["action 1", "action 2", "action 3"]

Only respond with the JSON array."""

        response = self.process(prompt)
        
        # Parse JSON response
        import json
        try:
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return []
        except Exception as e:
            logger.error(f"Failed to parse action items: {e}")
            return []
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"AIBrain(type={self.brain_type})"


def get_brain() -> AIBrain:
    """
    Get the AI Brain instance.
    
    Returns:
        Configured AIBrain instance
    """
    return AIBrain()


if __name__ == "__main__":
    # Test the AI Brain
    print("Testing AI Brain...")
    
    try:
        brain = AIBrain()
        print(f"✓ AI Brain initialized: {brain}")
        
        # Test basic processing
        print("\nTesting basic processing...")
        response = brain.process("Hello! What can you help me with?")
        print(f"Response: {response[:200]}...")
        
        # Test classification
        print("\nTesting classification...")
        test_item = """
---
type: email
from: boss@company.com
subject: Urgent: Project Deadline
---

Please complete the project by tomorrow. This is urgent!
"""
        classification = brain.classify_item(test_item)
        print(f"Classification: {classification}")
        
        print("\n✓ AI Brain tests completed!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check .env file exists with AI_BRAIN setting")
        print("2. Check processor files exist (claude_processor.py or qwen_processor.py)")
        print("3. Check dependencies are installed")
        sys.exit(1)
