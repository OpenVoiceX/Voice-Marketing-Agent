#!/usr/bin/env python3
"""
Test script to verify sequential calling functionality
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def test_sequential_calling():
    """Test the sequential calling functionality"""
    
    print("🧪 Testing Sequential Calling Functionality")
    print("=" * 50)
    
    # 1. Get campaign details
    print("\n1. Fetching campaign details...")
    try:
        response = requests.get(f"{API_BASE_URL}/campaigns/4")
        campaign = response.json()
        print(f"✅ Campaign: {campaign['name']} (ID: {campaign['id']})")
        print(f"📊 Contacts: {len(campaign['contacts'])}")
        
        # Show initial status
        for contact in campaign['contacts']:
            print(f"   - {contact['phone_number']}: {contact['status']}")
        
    except Exception as e:
        print(f"❌ Failed to fetch campaign: {e}")
        return
    
    # 2. Start the campaign
    print(f"\n2. Starting campaign...")
    try:
        response = requests.post(f"{API_BASE_URL}/campaigns/4/start")
        result = response.json()
        print(f"✅ {result['message']}")
        
    except Exception as e:
        print(f"❌ Failed to start campaign: {e}")
        return
    
    # 3. Monitor progress
    print(f"\n3. Monitoring call progress...")
    print("⏳ Waiting for calls to start...")
    time.sleep(5)  # Wait for first call to start
    
    for i in range(10):  # Monitor for up to 10 iterations
        try:
            # Get campaign status
            response = requests.get(f"{API_BASE_URL}/campaigns/4/status")
            status = response.json()
            
            print(f"\n📊 Status Update {i+1}:")
            print(f"   Campaign Status: {status['campaign_status']}")
            print(f"   Status Breakdown: {status['status_breakdown']}")
            
            # Check if all calls are done
            total_calls = sum(status['status_breakdown'].values())
            completed_calls = status['status_breakdown'].get('completed', 0) + status['status_breakdown'].get('failed', 0)
            
            if completed_calls >= total_calls:
                print(f"✅ All calls completed! ({completed_calls}/{total_calls})")
                break
            
            # Wait before next check
            print("⏳ Waiting 15 seconds for next update...")
            time.sleep(15)
            
        except Exception as e:
            print(f"❌ Failed to get status: {e}")
            break
    
    # 4. Final status
    print(f"\n4. Final campaign status...")
    try:
        response = requests.get(f"{API_BASE_URL}/campaigns/4")
        campaign = response.json()
        
        print(f"📊 Final Contact Status:")
        for contact in campaign['contacts']:
            print(f"   - {contact['phone_number']}: {contact['status']}")
        
    except Exception as e:
        print(f"❌ Failed to get final status: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Sequential calling test completed!")

def test_twilio_verification():
    """Test Twilio phone number verification"""
    
    print("\n🔧 Testing Twilio Phone Number Verification")
    print("=" * 40)
    
    # Test with a verified number (you need to add your verified number here)
    test_number = "+91 7206139480"  # Replace with your verified number
    
    try:
        test_data = {
            "to_number": test_number,
            "agent_id": 2
        }
        
        response = requests.post(f"{API_BASE_URL}/calls/originate", json=test_data)
        
        if response.status_code == 200:
            print(f"✅ Verified number {test_number} works!")
        elif response.status_code == 400:
            error = response.json()
            if "unverified" in error.get('detail', '').lower():
                print(f"❌ Number {test_number} is not verified in Twilio")
                print("   To fix this:")
                print("   1. Go to Twilio Console")
                print("   2. Navigate to Phone Numbers > Manage > Verified Caller IDs")
                print("   3. Add your phone number for verification")
            else:
                print(f"⚠️  Other error: {error.get('detail')}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Failed to test verification: {e}")

if __name__ == "__main__":
    print("🚀 Voice Marketing Agent - Sequential Calling Test")
    print("Make sure the backend is running on http://localhost:8000")
    
    # Test Twilio verification first
    test_twilio_verification()
    
    # Test sequential calling
    test_sequential_calling() 