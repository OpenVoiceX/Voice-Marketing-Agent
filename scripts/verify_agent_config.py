#!/usr/bin/env python3
"""
Verification script for per-agent configuration feature.
Run this after starting the backend to verify all components are working.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_agent_options():
    """Test the agent options endpoint."""
    print("🔍 Testing agent options endpoint...")
    response = requests.get(f"{BASE_URL}/agents/options/config")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Agent options endpoint working!")
        print(f"   - LLM Providers: {len(data['llm_providers'])}")
        print(f"   - STT Providers: {len(data['stt_providers'])}")
        print(f"   - TTS Voices: {len(data['tts_voices'])}")
        return True
    else:
        print(f"❌ Failed to get agent options: {response.status_code}")
        return False

def test_create_agent_with_config():
    """Test creating an agent with custom configuration."""
    print("\n🔍 Testing agent creation with custom config...")
    
    agent_data = {
        "name": "Test Agent - Groq + Josh",
        "system_prompt": "You are a helpful AI assistant for appointment setting.",
        "voice_id": "test_voice",
        "llm_provider": "groq",
        "llm_model": "llama-3.1-70b-versatile",
        "tts_voice_id": "TxGEqnHWrfWFTfGW9XjX",  # Josh voice
        "stt_provider": "deepgram"
    }
    
    response = requests.post(f"{BASE_URL}/agents/", json=agent_data)
    
    if response.status_code == 201:
        agent = response.json()
        print("✅ Agent created successfully!")
        print(f"   - ID: {agent['id']}")
        print(f"   - LLM: {agent.get('llm_provider', 'N/A')} ({agent.get('llm_model', 'N/A')})")
        print(f"   - Voice: {agent.get('tts_voice_id', 'N/A')[:20]}...")
        print(f"   - STT: {agent.get('stt_provider', 'N/A')}")
        return agent['id']
    else:
        print(f"❌ Failed to create agent: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_get_agent(agent_id):
    """Test retrieving an agent with configuration."""
    print(f"\n🔍 Testing agent retrieval (ID: {agent_id})...")
    
    response = requests.get(f"{BASE_URL}/agents/{agent_id}")
    
    if response.status_code == 200:
        agent = response.json()
        print("✅ Agent retrieved successfully!")
        print(f"   - Name: {agent['name']}")
        print(f"   - LLM Provider: {agent.get('llm_provider', 'NOT SET')}")
        print(f"   - LLM Model: {agent.get('llm_model', 'NOT SET')}")
        print(f"   - TTS Voice: {agent.get('tts_voice_id', 'NOT SET')}")
        print(f"   - STT Provider: {agent.get('stt_provider', 'NOT SET')}")
        
        # Verify all fields are present
        required_fields = ['llm_provider', 'llm_model', 'tts_voice_id', 'stt_provider']
        missing = [f for f in required_fields if f not in agent or agent[f] is None]
        
        if missing:
            print(f"⚠️  Warning: Missing fields: {missing}")
            return False
        else:
            print("✅ All configuration fields present!")
            return True
    else:
        print(f"❌ Failed to get agent: {response.status_code}")
        return False

def run_verification():
    """Run all verification tests."""
    print("=" * 60)
    print("Per-Agent Configuration Verification")
    print("=" * 60)
    
    results = []
    
    # Test 1: Options endpoint
    results.append(("Options Endpoint", test_agent_options()))
    
    # Test 2: Create agent with config
    agent_id = test_create_agent_with_config()
    results.append(("Create Agent", agent_id is not None))
    
    # Test 3: Retrieve agent (only if creation succeeded)
    if agent_id:
        results.append(("Retrieve Agent", test_get_agent(agent_id)))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Per-agent configuration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        success = run_verification()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend.")
        print("   Make sure the backend is running on http://localhost:8000")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
