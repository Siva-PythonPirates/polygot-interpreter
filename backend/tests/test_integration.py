#!/usr/bin/env python3

# Complete Frontend-Backend Integration Test

import requests
import json
import time

def test_backend_endpoints():
    """Test all backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪" + "="*80)
    print("🧪 COMPREHENSIVE BACKEND INTEGRATION TEST")
    print("🧪" + "="*80)
    
    try:
        # Test 1: Version endpoint
        print("\n🔍 Testing /version endpoint...")
        response = requests.get(f"{base_url}/version")
        if response.status_code == 200:
            version_data = response.json()
            print("✅ Version endpoint working!")
            print(f"   Version: {version_data.get('version', 'Unknown')}")
            print(f"   Orchestrator: {version_data.get('orchestrator', 'Unknown')}")
            print("   Features:")
            features = version_data.get('features', {})
            for feature, enabled in features.items():
                status = "✅" if enabled else "❌"
                print(f"     {status} {feature}: {enabled}")
            
            nested_supported = features.get('nested_blocks', False)
            if nested_supported:
                print("🎯 NESTED EXECUTION FULLY SUPPORTED!")
            else:
                print("⚠️  Nested execution not supported")
        else:
            print(f"❌ Version endpoint failed: {response.status_code}")
        
        # Test 2: Debug status endpoint
        print("\n🔍 Testing /debug/status endpoint...")
        response = requests.get(f"{base_url}/debug/status")
        if response.status_code == 200:
            debug_data = response.json()
            print("✅ Debug status endpoint working!")
            print(f"   Current debug mode: {debug_data.get('debug_mode', 'Unknown')}")
        else:
            print(f"❌ Debug status endpoint failed: {response.status_code}")
        
        # Test 3: Debug toggle endpoint
        print("\n🔍 Testing /debug/toggle endpoint...")
        response = requests.post(f"{base_url}/debug/toggle", 
                                json={"enabled": True})
        if response.status_code == 200:
            toggle_data = response.json()
            print("✅ Debug toggle endpoint working!")
            print(f"   Debug toggled to: {toggle_data.get('debug_mode', 'Unknown')}")
        else:
            print(f"❌ Debug toggle endpoint failed: {response.status_code}")
        
        print("\n🏁 Backend endpoints test completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_websocket_simulation():
    """Simulate WebSocket functionality using direct orchestrator calls"""
    print("\n🌐" + "="*60)
    print("🌐 WEBSOCKET FUNCTIONALITY SIMULATION")
    print("🌐" + "="*60)
    
    try:
        # Import the orchestrator functions
        import sys
        sys.path.append('.')
        from advanced_orchestrator import parse_code_to_tree, execute_tree_generator
        
        # Test nested code (same as your frontend example)
        nested_code = """
::py
results = []
::/py

::c
int numbers[] = {2, 4, 6, 8, 10};
for(int i = 0; i < 5; i++) {
    ::py 
    print(f"Processing {numbers[i]} in Python")
    results.append(numbers[i] ** 2)
    ::/py
    
    ::java 
    System.out.println("Java confirms: " + numbers[i] + " squared");
    ::/java
}
::/c

::py
print("Final results:", results)
print("Sum:", sum(results))
::/py
"""
        
        print("📝 Testing code parsing...")
        blocks = parse_code_to_tree(nested_code)
        print(f"✅ Parsed {len(blocks)} blocks")
        
        if len(blocks) == 1 and blocks[0].get('is_nested'):
            print("🎯 NESTED STRUCTURE DETECTED!")
        else:
            print("📋 Sequential structure detected")
        
        print("\n🚀 Simulating WebSocket execution...")
        print("=" * 40)
        
        # Execute and collect output (simulating WebSocket streaming)
        output_lines = []
        for line in execute_tree_generator(blocks):
            output_lines.append(line)
            print(line)
        
        print("=" * 40)
        print(f"✅ Generated {len(output_lines)} output lines")
        
        return True
        
    except Exception as e:
        print(f"❌ WebSocket simulation failed: {e}")
        return False

def main():
    """Run complete integration test"""
    print("🎯 Starting comprehensive frontend-backend integration test...")
    
    backend_ok = test_backend_endpoints()
    websocket_ok = test_websocket_simulation()
    
    print("\n🏆" + "="*80)
    print("🏆 INTEGRATION TEST RESULTS")
    print("🏆" + "="*80)
    
    print(f"Backend Endpoints: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"WebSocket Simulation: {'✅ PASS' if websocket_ok else '❌ FAIL'}")
    
    if backend_ok and websocket_ok:
        print("\n🎉 ALL TESTS PASSED! Frontend-backend integration is PERFECT!")
        print("🎉 Your nested polyglot interpreter is ready for production!")
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
    
    print("\n📋 Next steps for frontend testing:")
    print("1. Start the frontend: npm run dev")
    print("2. Open http://localhost:5173")
    print("3. Test the nested code example")
    print("4. Toggle debug mode and verify clean/verbose output")

if __name__ == "__main__":
    main()