from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import os

load_dotenv()


mcp = FastMCP("Todo")

token = os.getenv('TOKEN')
base_url = "https://thetodaytodo.netlify.app/api"
headers = {
    'Cookie': f'token={token}',
    'Content-Type': 'application/json'
}

@mcp.resource("todo://")
def get_todo_list() -> List[Dict[str, Any]]:
    """
    Get the todo list from the server.
    """
    endpoint = f"{base_url}/todos"
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        error_msg = response.json().get('error', 'Unknown error')
        raise Exception(f"Failed to get todos: {error_msg}")
    
    return response.json()

@mcp.tool()
def delete_todo(todo_id: str) -> bool:
    """
    Delete a todo
    
    Args:
        todo_id: ID of the todo to delete
        
    Returns:
        True if deletion was successful
    """
    endpoint = f"{base_url}/todos/{todo_id}"
    response = requests.delete(endpoint, headers=headers)
    
    if response.status_code != 200:
        error_msg = response.json().get('error', 'Unknown error')
        raise Exception(f"Failed to delete todo: {error_msg}")
    
    return True

@mcp.tool()
def create_todo(title: str, description: Optional[str] = None, 
                deadline: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new todo
    
    Args:
        title: Title of the todo
        description: Optional description of the todo
        deadline: Optional deadline in ISO format (e.g., '2025-05-01T12:00:00Z')
        
    Returns:
        The created todo as a dictionary
    """
    endpoint = f"{base_url}/todos"
    data = {
        "title": title,
        "description": description,
        "deadline": deadline
    }
    
    data = {k: v for k, v in data.items() if v is not None}
    
    response = requests.post(endpoint, headers=headers, json=data)
    
    if response.status_code != 201:
        error_msg = response.json().get('error', 'Unknown error')
        raise Exception(f"Failed to create todo: {error_msg}")
    
    return response.json()

@mcp.tool()
def update_todo(todo_id: str, title: Optional[str] = None,
                description: Optional[str] = None, completed: Optional[bool] = None,
                deadline: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing todo
    
    Args:
        todo_id: ID of the todo to update
        title: Optional new title
        description: Optional new description
        completed: Optional completion status
        deadline: Optional new deadline in ISO format
        
    Returns:
        The updated todo as a dictionary
    """
    endpoint = f"{base_url}/todos/{todo_id}"
    data = {
        "title": title,
        "description": description,
        "completed": completed,
        "deadline": deadline
    }
    
    data = {k: v for k, v in data.items() if v is not None}
    
    response = requests.put(endpoint, headers=headers, json=data)
    
    if response.status_code != 200:
        error_msg = response.json().get('error', 'Unknown error')
        raise Exception(f"Failed to update todo: {error_msg}")
    
    return response.json()

@mcp.tool()
def complete_todo(todo_id: str) -> Dict[str, Any]:
    """
    Mark a todo as completed
    
    Args:
        todo_id: ID of the todo to mark as completed
        
    Returns:
        The updated todo as a dictionary
    """
    return update_todo(todo_id, completed=True)



