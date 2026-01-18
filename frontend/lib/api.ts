/**
 * API client for Todo App
 */

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

const API_BASE_URL = 'http://localhost:8000';

export const taskAPI = {
  // Get all tasks for a user
  async getTasks(userId: string): Promise<Task[]> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`);
    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }
    return response.json();
  },

  // Get a single task
  async getTask(userId: string, taskId: number): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch task: ${response.statusText}`);
    }
    return response.json();
  },

  // Create a new task
  async createTask(userId: string, task: TaskCreate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });
    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.statusText}`);
    }
    return response.json();
  },

  // Update a task
  async updateTask(userId: string, taskId: number, updates: TaskUpdate): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });
    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.statusText}`);
    }
    return response.json();
  },

  // Delete a task
  async deleteTask(userId: string, taskId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }
  },

  // Chat with AI
  async chat(userId: string, message: string, conversationId?: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });
    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`);
    }
    return response.json();
  },
};
