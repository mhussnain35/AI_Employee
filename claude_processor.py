#!/usr/bin/env python3
"""
Claude Code Processor for AI Employee

This module integrates Claude Code CLI as the AI reasoning engine.
It handles all communication with Claude Code and processes responses.

Prerequisites:
- Claude Code CLI installed (https://claude.com/claude-code)
- Claude Code authenticated (run: claude login)

Configuration (in .env):
    AI_BRAIN=claude
    CLAUDE_MODEL=claude-sonnet-4-20250514
    CLAUDE_MAX_TOKENS=4096
    CLAUDE_TIMEOUT=300
"""

import os
import subprocess
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class ClaudeProcessor:
    """
    Claude Code processor for AI reasoning.
    
    Uses Claude Code CLI to process prompts and generate responses.
    Supports both CLI and API modes.
    """
    
    def __init__(self):
        """Initialize the Claude processor."""
        # Load configuration from environment
        self.model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
        self.max_tokens = int(os.getenv('CLAUDE_MAX_TOKENS', '4096'))
        self.timeout = int(os.getenv('CLAUDE_TIMEOUT', '300'))
        
        # Check if Claude Code CLI is available
        self.cli_available = self._check_cli()
        
        # API configuration (optional fallback)
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.base_url = os.getenv('CLAUDE_BASE_URL', 'https://api.anthropic.com')
        
        if not self.cli_available and not self.api_key:
            logger.warning("Claude Code CLI not found and no API key provided")
            logger.warning("Please install Claude Code CLI or set CLAUDE_API_KEY")
        
        logger.info(f"Claude processor initialized (CLI: {self.cli_available}, API: {bool(self.api_key)})")
    
    def _check_cli(self) -> bool:
        """Check if Claude Code CLI is available."""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def process(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Process a prompt with Claude Code.
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Returns:
            Claude's response as string
            
        Raises:
            RuntimeError: If neither CLI nor API is available
        """
        # Try CLI first, then API
        if self.cli_available:
            return self._process_cli(prompt, context)
        elif self.api_key:
            return self._process_api(prompt, context)
        else:
            raise RuntimeError(
                "No Claude method available. "
                "Install Claude Code CLI (https://claude.com/claude-code) "
                "or set CLAUDE_API_KEY in .env"
            )
    
    def _process_cli(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Process prompt using Claude Code CLI.
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Returns:
            Claude's response
        """
        logger.info("Processing with Claude Code CLI...")
        
        try:
            # Build the command
            cmd = [
                'claude',
                '--prompt', prompt,
                '--model', self.model,
                '--max-tokens', str(self.max_tokens)
            ]
            
            # Add context if provided
            if context:
                # Write context to temporary file
                import tempfile
                import json
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    json.dump(context, f)
                    context_file = f.name
                
                cmd.extend(['--context', context_file])
            
            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Clean up context file
            if context:
                try:
                    os.unlink(context_file)
                except:
                    pass
            
            # Check for errors
            if result.returncode != 0:
                logger.error(f"Claude CLI error: {result.stderr}")
                raise RuntimeError(f"Claude CLI error: {result.stderr}")
            
            logger.info(f"Claude CLI response: {len(result.stdout)} characters")
            return result.stdout
            
        except subprocess.TimeoutExpired:
            logger.error(f"Claude CLI timeout after {self.timeout}s")
            raise RuntimeError(f"Claude CLI timeout after {self.timeout}s")
        except FileNotFoundError:
            logger.error("Claude CLI not found")
            raise RuntimeError("Claude CLI not found. Please install from https://claude.com/claude-code")
        except Exception as e:
            logger.error(f"Claude CLI error: {e}")
            raise
    
    def _process_api(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Process prompt using Claude API (fallback method).
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Returns:
            Claude's response
        """
        logger.info("Processing with Claude API...")
        
        try:
            import requests
            
            # Build the request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}',
                'x-api-key': self.api_key
            }
            
            data = {
                'model': self.model,
                'max_tokens': self.max_tokens,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            }
            
            # Add context if provided
            if context:
                system_context = f"Context: {json.dumps(context)}"
                data['messages'].insert(0, {
                    'role': 'system',
                    'content': system_context
                })
            
            # Make the request
            response = requests.post(
                f"{self.base_url}/v1/messages",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Extract response
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            if not content:
                logger.error("Empty response from Claude API")
                raise RuntimeError("Empty response from Claude API")
            
            logger.info(f"Claude API response: {len(content)} characters")
            return content
            
        except ImportError:
            logger.error("requests library not installed")
            logger.error("Install with: pip install requests")
            raise RuntimeError("requests library not installed")
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def stream(self, prompt: str, context: Optional[dict] = None):
        """
        Stream a prompt with Claude Code (interactive mode).
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Yields:
            Chunks of Claude's response
        """
        logger.info("Streaming with Claude Code CLI...")
        
        if not self.cli_available:
            raise RuntimeError("Claude CLI required for streaming")
        
        try:
            # Build the command
            cmd = [
                'claude',
                '--prompt', prompt,
                '--model', self.model,
                '--stream'  # Enable streaming
            ]
            
            # Run the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Stream the output
            for line in process.stdout:
                yield line.strip()
            
            # Check for errors
            process.wait()
            if process.returncode != 0:
                error = process.stderr.read()
                logger.error(f"Claude CLI error: {error}")
                raise RuntimeError(f"Claude CLI error: {error}")
                
        except Exception as e:
            logger.error(f"Claude streaming error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Claude is available (CLI or API)."""
        return self.cli_available or bool(self.api_key)


if __name__ == "__main__":
    # Test the Claude processor
    print("Testing Claude Processor...")
    
    processor = ClaudeProcessor()
    print(f"✓ Claude processor initialized")
    print(f"  CLI available: {processor.cli_available}")
    print(f"  API available: {bool(processor.api_key)}")
    
    if processor.is_available():
        print("\nTesting basic processing...")
        try:
            response = processor.process("Hello! What can you help me with?")
            print(f"Response: {response[:200]}...")
            print("\n✓ Claude processor test completed!")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    else:
        print("\n⚠ Claude not available")
        print("Install Claude Code CLI: https://claude.com/claude-code")
        print("Or set CLAUDE_API_KEY in .env file")
