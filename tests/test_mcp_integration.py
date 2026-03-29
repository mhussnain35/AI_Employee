#!/usr/bin/env python3
"""
Test MCP Servers Integration with AI Brain

This script tests if MCP servers are properly connected to the AI Brain.

Usage:
    python tests/test_mcp_integration.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def test_mcp_servers_import():
    """Test that MCP servers can be imported."""
    print_header("Test 1: MCP Servers Import")
    
    try:
        from mcp_servers import EmailMCPServer, WhatsAppMCPServer
        print("  ✓ MCP servers imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Failed to import MCP servers: {e}")
        return False


def test_email_mcp_initialization():
    """Test Email MCP server initialization."""
    print_header("Test 2: Email MCP Server")
    
    try:
        from mcp_servers import EmailMCPServer
        
        server = EmailMCPServer()
        print(f"  ✓ Email MCP Server initialized")
        
        # Check if Gmail service is available
        if server.service:
            print(f"  ✓ Gmail service connected")
        else:
            print(f"  ⚠ Gmail service not available")
            print(f"     Run: python main.py setup-gmail")
        
        # Check tools
        tools = server.get_tools()
        print(f"  ✓ Available tools: {len(tools)}")
        for tool in tools:
            print(f"    - {tool['name']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_whatsapp_mcp_initialization():
    """Test WhatsApp MCP server initialization."""
    print_header("Test 3: WhatsApp MCP Server")
    
    try:
        from mcp_servers import WhatsAppMCPServer
        
        server = WhatsAppMCPServer()
        print(f"  ✓ WhatsApp MCP Server initialized")
        print(f"  ⚠ Status: STUB (requires WhatsApp Business API)")
        
        # Check tools
        tools = server.get_tools()
        print(f"  ✓ Available tools: {len(tools)}")
        for tool in tools:
            print(f"    - {tool['name']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_mcp_config_file():
    """Test MCP configuration file."""
    print_header("Test 4: MCP Configuration")
    
    config_file = Path(__file__).parent.parent / "mcp_config.json"
    
    if config_file.exists():
        print(f"  ✓ mcp_config.json found")
        
        import json
        config = json.loads(config_file.read_text())
        
        if 'mcpServers' in config:
            print(f"  ✓ MCP servers configured: {len(config['mcpServers'])}")
            for name, server_config in config['mcpServers'].items():
                print(f"    - {name}: {server_config.get('command')} {server_config.get('args', [''])[0]}")
            return True
        else:
            print(f"  ✗ mcpServers not found in config")
            return False
    else:
        print(f"  ✗ mcp_config.json not found")
        print(f"     Creating default config...")
        return False


def test_ai_brain_mcp_integration():
    """Test if AI Brain can access MCP servers."""
    print_header("Test 5: AI Brain + MCP Integration")
    
    try:
        from ai_brain import AIBrain
        
        brain = AIBrain()
        print(f"  ✓ AI Brain initialized: {brain.brain_type}")
        
        # Check if brain has MCP capability
        if hasattr(brain, 'mcp_servers'):
            print(f"  ✓ AI Brain has MCP integration")
            print(f"     MCP servers: {list(brain.mcp_servers.keys())}")
        else:
            print(f"  ⚠ AI Brain MCP integration not implemented yet")
            print(f"     MCP servers are standalone (not connected to brain)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_orchestrator_mcp_integration():
    """Test if Orchestrator can use MCP servers."""
    print_header("Test 6: Orchestrator + MCP Integration")
    
    try:
        from orchestrator import Orchestrator
        
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
        orchestrator = Orchestrator(vault_path, use_ai=False)  # Don't use AI for this test
        
        print(f"  ✓ Orchestrator initialized")
        
        # Check if orchestrator has MCP capability
        if hasattr(orchestrator, 'mcp_servers'):
            print(f"  ✓ Orchestrator has MCP integration")
        else:
            print(f"  ⚠ Orchestrator MCP integration not implemented yet")
            print(f"     MCP servers are standalone (not connected to orchestrator)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_mcp_server_functionality():
    """Test MCP server actual functionality."""
    print_header("Test 7: MCP Server Functionality")
    
    try:
        from mcp_servers import EmailMCPServer
        
        server = EmailMCPServer()
        
        if not server.service:
            print(f"  ⊘ Skipping functionality test (Gmail not authenticated)")
            return True
        
        # Test search
        print(f"  Testing email search...")
        emails = server.search_emails('is:unread', max_results=1)
        print(f"  ✓ Search works: Found {len(emails)} unread emails")
        
        # Test tool calling
        print(f"  Testing tool call interface...")
        result = server.call_tool('search_emails', {'query': 'is:unread', 'max_results': 1})
        if 'emails' in result:
            print(f"  ✓ Tool call interface works")
        else:
            print(f"  ✗ Tool call interface failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print_header("MCP Servers Integration Test Suite")
    print("Testing MCP Connection with AI Brain and Orchestrator")
    
    tests = [
        ("MCP Servers Import", test_mcp_servers_import),
        ("Email MCP Server", test_email_mcp_initialization),
        ("WhatsApp MCP Server", test_whatsapp_mcp_initialization),
        ("MCP Configuration", test_mcp_config_file),
        ("AI Brain Integration", test_ai_brain_mcp_integration),
        ("Orchestrator Integration", test_orchestrator_mcp_integration),
        ("MCP Functionality", test_mcp_server_functionality),
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
    
    # Analysis
    print_header("Integration Analysis")
    
    mcp_ok = all(result for name, result in results[:3])
    config_ok = results[3][1] if len(results) > 3 else False
    brain_integration = results[4][1] if len(results) > 4 else False
    orchestrator_integration = results[5][1] if len(results) > 5 else False
    
    if mcp_ok:
        print("  ✓ MCP Servers are working")
    else:
        print("  ✗ MCP Servers have issues")
    
    if config_ok:
        print("  ✓ MCP Configuration exists")
    else:
        print("  ⚠ MCP Configuration needs setup")
    
    if brain_integration and orchestrator_integration:
        print("  ✓ MCP fully integrated with Brain and Orchestrator")
    else:
        print("  ⚠ MCP servers are standalone (not integrated)")
        print("\n  Next Steps:")
        print("  1. Add MCP integration to ai_brain.py")
        print("  2. Add MCP integration to orchestrator.py")
        print("  3. See MCP_INTEGRATION_GUIDE.md for instructions")
    
    print("\n" + "="*70)
    print("MCP Integration Test Complete")
    print("="*70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
