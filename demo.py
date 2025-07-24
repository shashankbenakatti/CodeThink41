import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_response(response, operation):
    print(f"\n{'='*50}")
    print(f"Operation: {operation}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")
        except:
            print(f"Response: {response.text}")
    else:
        print(f"Error: {response.text}")
    print(f"{'='*50}")

def demonstrate_api():
    print("🚀 Starting Code Snippets API Demonstration")
    
    # Test user ID
    user_id = "john_doe"
    
    # 1. Create/Update snippets
    print("\n📝 Creating code snippets...")
    
    # Python snippet
    python_snippet = {
        "snippet_name": "hello_world",
        "language": "python",
        "code_content": "def hello():\n    print('Hello, World!')\n\nhello()"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/snippets", json=python_snippet)
    print_response(response, "Create Python Snippet")
    
    # JavaScript snippet
    js_snippet = {
        "snippet_name": "fetch_data",
        "language": "javascript",
        "code_content": "async function fetchData(url) {\n    const response = await fetch(url);\n    return response.json();\n}"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/snippets", json=js_snippet)
    print_response(response, "Create JavaScript Snippet")
    
    # SQL snippet
    sql_snippet = {
        "snippet_name": "user_query",
        "language": "sql",
        "code_content": "SELECT u.id, u.name, COUNT(s.id) as snippet_count\nFROM users u\nLEFT JOIN snippets s ON u.id = s.user_id\nGROUP BY u.id, u.name;"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/snippets", json=sql_snippet)
    print_response(response, "Create SQL Snippet")
    
    # Another Python snippet
    python_snippet2 = {
        "snippet_name": "fibonacci",
        "language": "python",
        "code_content": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/snippets", json=python_snippet2)
    print_response(response, "Create Another Python Snippet")
    
    # 2. List all snippets for user
    print("\n📋 Listing all snippets for user...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/snippets")
    print_response(response, "List All User Snippets")
    
    # 3. Get specific snippet
    print("\n🔍 Getting specific snippet...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/snippets/hello_world")
    print_response(response, "Get Specific Snippet (hello_world)")
    
    # 4. Update existing snippet
    print("\n✏️ Updating existing snippet...")
    updated_snippet = {
        "snippet_name": "hello_world",
        "language": "python",
        "code_content": "def hello(name='World'):\n    print(f'Hello, {name}!')\n\nhello('FastAPI')\nhello()"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id}/snippets", json=updated_snippet)
    print_response(response, "Update Existing Snippet")
    
    # 5. Get snippets by language
    print("\n🔍 Getting snippets by language (Python)...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/snippets/language/python")
    print_response(response, "Get Python Snippets")
    
    # 6. Test with another user
    print("\n👤 Testing with another user...")
    user_id2 = "jane_smith"
    
    java_snippet = {
        "snippet_name": "hello_java",
        "language": "java",
        "code_content": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, Java!\");\n    }\n}"
    }
    
    response = requests.post(f"{BASE_URL}/users/{user_id2}/snippets", json=java_snippet)
    print_response(response, "Create Java Snippet for Another User")
    
    response = requests.get(f"{BASE_URL}/users/{user_id2}/snippets")
    print_response(response, "List Snippets for Another User")
    
    # 7. Test error case - get non-existent snippet
    print("\n❌ Testing error case...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/snippets/nonexistent")
    print_response(response, "Get Non-existent Snippet (Should be 404)")
    
    # 8. Delete a snippet
    print("\n🗑️ Deleting a snippet...")
    response = requests.delete(f"{BASE_URL}/users/{user_id}/snippets/fibonacci")
    print_response(response, "Delete Snippet")
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/users/{user_id}/snippets")
    print_response(response, "List Snippets After Deletion")
    
    print("\n✅ API Demonstration Complete!")
    print("\nTo explore the API interactively, visit: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        # Test if server is running
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            demonstrate_api()
        else:
            print("❌ Server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure to start the FastAPI server first:")
        print("   python main.py")
        print("\nOr run with uvicorn:")
        print("   uvicorn main:app --reload")
