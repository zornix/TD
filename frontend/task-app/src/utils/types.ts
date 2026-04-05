export interface Category {
  id: number;
  name: string;
  coefficient: number;
  created_at?: string;
  updated_at?: string;
}

export interface Task {
  id: number;
  description: string;
  is_done: boolean;
  due_date: string | null;
  estimated_effort_hours: number | null;
  importance: number;
  category_id: number;
  urgency_score: number;
  imp_score: number;
  quadrant: string | null;
  created_at: string;
  updated_at: string;
}
