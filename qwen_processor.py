#!/usr/bin/env python3
"""
Qwen API Processor for AI Employee

This module integrates Qwen API (Alibaba Cloud) as the AI reasoning engine.
It handles all communication with Qwen API and processes responses.

Prerequisites:
- Qwen API key from Alibaba Cloud (https://dashscope.aliyun.com/)
- requests library installed

Configuration (in .env):
    AI_BRAIN=qwen
    QWEN_API_KEY=your-api-key
    QWEN_MODEL=qwen-plus
    QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
    QWEN_MAX_TOKENS=4096
    QWEN_TIMEOUT=300
"""

import os
import json
import logging
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class QwenProcessor:
    """
    Qwen API processor for AI reasoning.
    
    Uses Qwen API (DashScope) to process prompts and generate responses.
    Supports OpenAI-compatible API format.
    """
    
    def __init__(self):
        """Initialize the Qwen processor."""
        # Load configuration from environment
        self.api_key = os.getenv('QWEN_API_KEY')
        self.model = os.getenv('QWEN_MODEL', 'qwen-plus')
        self.base_url = os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.max_tokens = int(os.getenv('QWEN_MAX_TOKENS', '4096'))
        self.timeout = int(os.getenv('QWEN_TIMEOUT', '300'))
        
        # Validate configuration
        if not self.api_key:
            logger.warning("QWEN_API_KEY not set in .env")
            logger.warning("Get API key from: https://dashscope.aliyun.com/")
        
        logger.info(f"Qwen processor initialized (model: {self.model})")
    
    def process(self, prompt: str, context: Optional[dict] = None) -> str:
        """
        Process a prompt with Qwen API.
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Returns:
            Qwen's response as string
            
        Raises:
            RuntimeError: If API key is missing or request fails
        """
        if not self.api_key:
            raise RuntimeError(
                "QWEN_API_KEY not set. "
                "Get API key from https://dashscope.aliyun.com/ "
                "and add to .env file"
            )
        
        logger.info(f"Processing with Qwen API ({self.model})...")
        
        try:
            import requests
            
            # Build the request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            # Build messages array
            messages = []
            
            # Add system context if provided
            if context:
                system_context = f"You are an AI Employee assistant. Context: {json.dumps(context)}"
                messages.append({
                    'role': 'system',
                    'content': system_context
                })
            
            # Add user prompt
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Build request body
            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': self.max_tokens,
                'temperature': 0.7,  # Balanced creativity/consistency
                'top_p': 0.9,
                'stream': False
            }
            
            # Make the request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Extract response
            result = response.json()
            
            # Handle different response formats
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
            elif 'data' in result and 'choices' in result['data']:
                content = result['data']['choices'][0]['message']['content']
            else:
                logger.error(f"Unexpected response format: {result.keys()}")
                raise RuntimeError(f"Unexpected response format from Qwen API")
            
            if not content:
                logger.error("Empty response from Qwen API")
                raise RuntimeError("Empty response from Qwen API")
            
            logger.info(f"Qwen API response: {len(content)} characters")
            return content
            
        except ImportError:
            logger.error("requests library not installed")
            logger.error("Install with: uv add requests")
            raise RuntimeError("requests library not installed")
        except requests.exceptions.Timeout:
            logger.error(f"Qwen API timeout after {self.timeout}s")
            raise RuntimeError(f"Qwen API timeout after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            logger.error(f"Qwen API request error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise RuntimeError(f"Qwen API error: {e}")
        except Exception as e:
            logger.error(f"Qwen API error: {e}")
            raise
    
    def stream(self, prompt: str, context: Optional[dict] = None):
        """
        Stream a prompt with Qwen API.
        
        Args:
            prompt: The prompt to process
            context: Optional context dictionary
            
        Yields:
            Chunks of Qwen's response
        """
        if not self.api_key:
            raise RuntimeError("QWEN_API_KEY not set")
        
        logger.info(f"Streaming with Qwen API ({self.model})...")
        
        try:
            import requests
            import sseclient
            
            # Build the request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            # Build messages array
            messages = []
            
            if context:
                system_context = f"Context: {json.dumps(context)}"
                messages.append({
                    'role': 'system',
                    'content': system_context
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Build request body for streaming
            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': self.max_tokens,
                'temperature': 0.7,
                'stream': True  # Enable streaming
            }
            
            # Make the streaming request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Process Server-Sent Events
            client = sseclient.SSEClient(response)
            
            for event in client.events():
                if event.data:
                    try:
                        data = json.loads(event.data)
                        if 'choices' in data and len(data['choices']) > 0:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        continue
                        
        except ImportError as e:
            logger.error(f"Streaming requires additional libraries: {e}")
            logger.error("Install with: uv add requests sseclient-py")
            raise RuntimeError("Streaming libraries not installed")
        except Exception as e:
            logger.error(f"Qwen streaming error: {e}")
            raise
    
    def chat(self, messages: list, **kwargs) -> str:
        """
        Send a chat conversation to Qwen API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters
            
        Returns:
            Qwen's response
        """
        if not self.api_key:
            raise RuntimeError("QWEN_API_KEY not set")
        
        logger.info(f"Processing chat with Qwen API ({self.model})...")
        
        try:
            import requests
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            # Build request body
            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': kwargs.get('max_tokens', self.max_tokens),
                'temperature': kwargs.get('temperature', 0.7),
                'stream': False
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                logger.info(f"Qwen chat response: {len(content)} characters")
                return content
            else:
                raise RuntimeError("No response from Qwen API")
                
        except Exception as e:
            logger.error(f"Qwen chat error: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Qwen API is available."""
        return bool(self.api_key)
    
    def test_connection(self) -> bool:
        """Test the connection to Qwen API."""
        try:
            response = self.process("Hello! Just testing the connection.")
            return len(response) > 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


if __name__ == "__main__":
    # Test the Qwen processor
    print("Testing Qwen Processor...")
    
    processor = QwenProcessor()
    print(f"✓ Qwen processor initialized")
    print(f"  Model: {processor.model}")
    print(f"  Base URL: {processor.base_url}")
    print(f"  API Key: {'Set' if processor.api_key else 'Not set'}")
    
    if processor.is_available():
        print("\nTesting basic processing...")
        try:
            response = processor.process("Hello! What can you help me with?")
            print(f"Response: {response[:200]}...")
            print("\n✓ Qwen processor test completed!")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    else:
        print("\n⚠ Qwen API not available")
        print("Get API key from: https://dashscope.aliyun.com/")
        print("Add to .env file: QWEN_API_KEY=your-api-key")
