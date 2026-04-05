// API Utility functions to interact with the FastAPI backend
// URL defaults to localhost:8000
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Handle API responses globally
 */
async function handleResponse(response: Response) {
  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `HTTP Error: ${response.status}`);
  }
  return response.json();
}

/**
 * Fetch all categories
 */
export async function getCategories() {
  const res = await fetch(`${API_BASE_URL}/categories`);
  return handleResponse(res);
}

/**
 * Create a new single category
 */
export async function createCategory(name: string, coefficient: number) {
  const res = await fetch(`${API_BASE_URL}/categories`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, coefficient })
  });
  return handleResponse(res);
}

/**
 * Fetch all tasks
 */
export async function getTasks() {
  const res = await fetch(`${API_BASE_URL}/tasks`);
  return handleResponse(res);
}

/**
 * Create a new task
 */
export async function createTask(taskData: {
  description: string;
  is_done?: boolean;
  due_date?: string | null;
  estimated_effort_hours?: number | null;
  importance: number;
  category_id: number;
}) {
  const res = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData)
  });
  return handleResponse(res);
}

/**
 * Toggle task done status
 */
export async function toggleTaskDone(taskId: number) {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}/done`, {
    method: 'PATCH'
  });
  return handleResponse(res);
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: number) {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'DELETE'
  });
  return handleResponse(res);
}
