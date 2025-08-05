#!/usr/bin/env python3
"""
Test script to verify campaign calling functionality
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def test_campaign_functionality():
    """Test the complete campaign workflow"""
    
    print("🧪 Testing Campaign Calling Functionality")
    print("=" * 50)
    
    # 1. Get all campaigns
    print("\n1. Fetching campaigns...")
    try:
        response = requests.get(f"{API_BASE_URL}/campaigns/")
        campaigns = response.json()
        print(f"✅ Found {len(campaigns)} campaigns")
        
        if not campaigns:
            print("❌ No campaigns found. Please create a campaign first.")
            return
            
        campaign = campaigns[0]  # Use the first campaign
        campaign_id = campaign['id']
        print(f"📋 Using campaign: {campaign['name']} (ID: {campaign_id})")
        
    except Exception as e:
        print(f"❌ Failed to fetch campaigns: {e}")
        return
    
    # 2. Check campaign status
    print(f"\n2. Checking campaign {campaign_id} status...")
    try:
        response = requests.get(f"{API_BASE_URL}/campaigns/{campaign_id}/status")
        status = response.json()
        print(f"✅ Campaign status: {status['campaign_status']}")
        print(f"📊 Contact breakdown: {status['status_breakdown']}")
        
    except Exception as e:
        print(f"❌ Failed to get campaign status: {e}")
    
    # 3. Test starting the campaign
    print(f"\n3. Testing campaign start...")
    try:
        response = requests.post(f"{API_BASE_URL}/campaigns/{campaign_id}/start")
        result = response.json()
        print(f"✅ {result['message']}")
        
        # Wait a moment for calls to be initiated
        print("⏳ Waiting 5 seconds for calls to be initiated...")
        time.sleep(5)
        
        # Check status again
        response = requests.get(f"{API_BASE_URL}/campaigns/{campaign_id}/status")
        status = response.json()
        print(f"📊 Updated status breakdown: {status['status_breakdown']}")
        
    except Exception as e:
        print(f"❌ Failed to start campaign: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response.text}")
    
    # 4. Test stopping the campaign
    print(f"\n4. Testing campaign stop...")
    try:
        response = requests.post(f"{API_BASE_URL}/campaigns/{campaign_id}/stop")
        result = response.json()
        print(f"✅ {result['message']}")
        
    except Exception as e:
        print(f"❌ Failed to stop campaign: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Campaign testing completed!")

def test_twilio_configuration():
    """Test if Twilio is properly configured"""
    
    print("\n🔧 Testing Twilio Configuration")
    print("=" * 30)
    
    try:
        # Test the originate call endpoint
        test_data = {
            "to_number": "+1234567890",  # Test number
            "agent_id": 1
        }
        
        response = requests.post(f"{API_BASE_URL}/calls/originate", json=test_data)
        
        if response.status_code == 400:
            error = response.json()
            if "TWILIO environment variables" in error.get('detail', ''):
                print("❌ Twilio not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
            else:
                print(f"⚠️  Twilio configured but test failed: {error.get('detail')}")
        elif response.status_code == 200:
            print("✅ Twilio appears to be configured correctly")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Failed to test Twilio configuration: {e}")

if __name__ == "__main__":
    print("🚀 Voice Marketing Agent - Campaign Test")
    print("Make sure the backend is running on http://localhost:8000")
    
    # Test Twilio configuration first
    test_twilio_configuration()
    
    # Test campaign functionality
    test_campaign_functionality() 