#!/usr/bin/env python3
"""
AI Brain Test Suite

Tests for Claude and Qwen AI brain implementations.

Usage:
    python test_ai_brain.py
"""

import sys
from pathlib import Path


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def test_env_configuration():
    """Test that .env file is properly configured."""
    print_header("Test 1: Environment Configuration")
    
    env_file = Path(__file__).parent / '.env'
    env_example = Path(__file__).parent / '.env.example'
    
    # Check .env.example exists
    if env_example.exists():
        print("  ✓ .env.example exists")
        
        content = env_example.read_text()
        if 'AI_BRAIN=' in content:
            print("  ✓ AI_BRAIN configuration found")
        else:
            print("  ✗ AI_BRAIN configuration missing")
            return False
            
        if 'CLAUDE_' in content:
            print("  ✓ Claude configuration found")
        else:
            print("  ✗ Claude configuration missing")
            return False
            
        if 'QWEN_' in content:
            print("  ✓ Qwen configuration found")
        else:
            print("  ✗ Qwen configuration missing")
            return False
    else:
        print("  ✗ .env.example not found")
        return False
    
    # Check .env exists
    if env_file.exists():
        print("  ✓ .env file exists")
        
        content = env_file.read_text()
        if 'AI_BRAIN=' in content:
            print("  ✓ AI_BRAIN is set")
        else:
            print("  ✗ AI_BRAIN not set")
            return False
    else:
        print("  ⚠ .env file not found (using defaults)")
    
    print("\n✓ Environment configuration test passed!")
    return True


def test_claude_processor():
    """Test Claude processor initialization."""
    print_header("Test 2: Claude Processor")
    
    try:
        from claude_processor import ClaudeProcessor
        
        processor = ClaudeProcessor()
        print(f"  ✓ Claude processor initialized")
        print(f"  Model: {processor.model}")
        print(f"  CLI available: {processor.cli_available}")
        print(f"  API available: {bool(processor.api_key)}")
        
        if processor.is_available():
            print("  ✓ Claude is available")
            return True
        else:
            print("  ⚠ Claude not available")
            print("\n  To enable Claude:")
            print("  1. Install Claude Code CLI: https://claude.com/claude-code")
            print("  2. Or set CLAUDE_API_KEY in .env")
            return False
            
    except ImportError as e:
        print(f"  ✗ Failed to import Claude processor: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_qwen_processor():
    """Test Qwen processor initialization."""
    print_header("Test 3: Qwen Processor")
    
    try:
        from qwen_processor import QwenProcessor
        
        processor = QwenProcessor()
        print(f"  ✓ Qwen processor initialized")
        print(f"  Model: {processor.model}")
        print(f"  Base URL: {processor.base_url}")
        print(f"  API Key: {'Set' if processor.api_key else 'Not set'}")
        
        if processor.is_available():
            print("  ✓ Qwen is available")
            
            # Test connection if API key is set
            if processor.api_key and processor.api_key != 'your-qwen-api-key-here':
                print("  Testing connection...")
                if processor.test_connection():
                    print("  ✓ Connection successful")
                else:
                    print("  ⚠ Connection failed")
                    return False
            
            return True
        else:
            print("  ⚠ Qwen not available")
            print("\n  To enable Qwen:")
            print("  1. Get API key from: https://dashscope.aliyun.com/")
            print("  2. Set QWEN_API_KEY in .env")
            print("  3. Set AI_BRAIN=qwen in .env")
            return False
            
    except ImportError as e:
        print(f"  ✗ Failed to import Qwen processor: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_ai_brain():
    """Test main AI Brain interface."""
    print_header("Test 4: AI Brain Interface")
    
    try:
        from ai_brain import AIBrain, get_brain
        
        # Test initialization
        brain = get_brain()
        print(f"  ✓ AI Brain initialized: {brain}")
        print(f"  Brain type: {brain.brain_type}")
        
        # Test processor
        if brain.processor:
            print(f"  ✓ Processor available: {type(brain.processor).__name__}")
        else:
            print("  ✗ Processor not available")
            return False
        
        return True
        
    except ImportError as e:
        print(f"  ✗ Failed to import AI Brain: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_ralph_wiggum():
    """Test Ralph Wiggum persistence loop."""
    print_header("Test 5: Ralph Wiggum Loop")
    
    try:
        from ralph_wiggum import RalphWiggumHook, RalphWiggumManager
        
        # Create test file
        test_dir = Path(__file__).parent / "AI_Employee_Vault" / "Needs_Action"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "TEST_RALPH.md"
        test_file.write_text("# Test")
        
        # Test hook
        hook = RalphWiggumHook(test_file, max_iterations=3)
        print(f"  ✓ Ralph Wiggum Hook created: {hook}")
        
        # Test iterations
        iterations = 0
        while hook.should_continue() and iterations < 5:
            iterations += 1
            hook.on_iteration_start()
            hook.on_iteration_complete("Test response")
        
        print(f"  ✓ Iterations completed: {iterations}")
        
        # Test manager
        manager = RalphWiggumManager()
        stats = manager.get_stats()
        print(f"  ✓ Ralph Wiggum Manager: {stats}")
        
        # Cleanup
        test_file.unlink()
        
        print("\n✓ Ralph Wiggum test passed!")
        return True
        
    except ImportError as e:
        print(f"  ✗ Failed to import Ralph Wiggum: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_orchestrator_integration():
    """Test orchestrator with AI brain integration."""
    print_header("Test 6: Orchestrator Integration")
    
    try:
        from orchestrator import Orchestrator
        
        vault_path = Path(__file__).parent / "AI_Employee_Vault"
        
        # Create orchestrator with AI
        orchestrator = Orchestrator(vault_path, use_ai=True)
        
        print(f"  ✓ Orchestrator created")
        print(f"  AI enabled: {orchestrator.use_ai}")
        if orchestrator.brain:
            print(f"  Brain type: {orchestrator.brain.brain_type}")
        
        # Check pending items
        pending = orchestrator.get_pending_items()
        print(f"  Pending items: {len(pending)}")
        
        print("\n✓ Orchestrator integration test passed!")
        return True
        
    except ImportError as e:
        print(f"  ✗ Failed to import Orchestrator: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print_header("AI Brain Test Suite")
    print("Testing Claude and Qwen AI Brain Implementations")
    
    tests = [
        ("Environment Configuration", test_env_configuration),
        ("Claude Processor", test_claude_processor),
        ("Qwen Processor", test_qwen_processor),
        ("AI Brain Interface", test_ai_brain),
        ("Ralph Wiggum Loop", test_ralph_wiggum),
        ("Orchestrator Integration", test_orchestrator_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Recommendations
    print_header("Recommendations")
    
    claude_ok = any('Claude' in name and result for name, result in results)
    qwen_ok = any('Qwen' in name and result for name, result in results)
    
    if claude_ok:
        print("  ✓ Claude is ready to use")
        print("    → Set AI_BRAIN=claude in .env")
    
    if qwen_ok:
        print("  ✓ Qwen is ready to use")
        print("    → Set AI_BRAIN=qwen in .env")
    
    if not claude_ok and not qwen_ok:
        print("  ⚠ No AI brain is fully configured")
        print("\n  To enable Claude:")
        print("    1. Install: https://claude.com/claude-code")
        print("    2. Set AI_BRAIN=claude in .env")
        print("\n  To enable Qwen:")
        print("    1. Get API key: https://dashscope.aliyun.com/")
        print("    2. Set QWEN_API_KEY in .env")
        print("    3. Set AI_BRAIN=qwen in .env")
    
    print("\n" + "="*70)
    print("AI Brain Test Complete")
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
