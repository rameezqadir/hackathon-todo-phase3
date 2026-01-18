"""Test script for Phase III chat functionality"""

import requests
import time

BASE_URL = "http://localhost:8000"
USER_ID = "test-user"

def test_chat():
    print("🧪 Testing Phase III Chat Endpoint")
    print("="*60)
    
    test_cases = [
        ("Add task: Buy groceries", ["add_task"]),
        ("What is on my list?", ["list_tasks"]),
        ("Add task: Call dentist", ["add_task"]),
        ("Show pending tasks", ["list_tasks"]),
        ("Mark task 1 as done", ["complete_task"]),
        ("Delete task 2", ["delete_task"]),
        ("Show all tasks", ["list_tasks"]),
    ]
    
    conversation_id = None
    passed = 0
    failed = 0
    
    for message, expected_tools in test_cases:
        print(f"\n📤 Sending: {message}")
        
        payload = {"message": message}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/{USER_ID}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                conversation_id = data["conversation_id"]
                
                print(f"✅ Response: {data['response']}")
                
                if data.get('tool_calls'):
                    print(f"🔧 Tools: {', '.join(data['tool_calls'])}")
                    
                    if set(data['tool_calls']) == set(expected_tools):
                        print(f"✅ Correct tools used")
                        passed += 1
                    else:
                        print(f"⚠️  Expected: {expected_tools}")
                        failed += 1
                else:
                    if expected_tools:
                        print(f"❌ No tools called (expected: {expected_tools})")
                        failed += 1
                    else:
                        passed += 1
            else:
                print(f"❌ Error: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            failed += 1
        
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    print("="*60)

if __name__ == "__main__":
    test_chat()
