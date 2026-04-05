'use client';

import React from 'react';
import { Task, Category } from '../utils/types';
import { toggleTaskDone, deleteTask } from '../utils/api';

interface TaskItemProps {
  task: Task;
  category?: Category;
  onUpdate: () => void;
}

export default function TaskItem({ task, category, onUpdate }: TaskItemProps) {
  const handleToggle = async () => {
    try {
      await toggleTaskDone(task.id);
      onUpdate();
    } catch (err) {
      console.error(err);
      alert('Failed to toggle task');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Delete this task?')) return;
    try {
      await deleteTask(task.id);
      onUpdate();
    } catch (err) {
      console.error(err);
      alert('Failed to delete task');
    }
  };

  // Extract quadrant visually if valid
  const isQuadValid = task.quadrant && task.quadrant !== 'None';
  
  return (
    <div className={`task-item glass-panel ${task.is_done ? 'task-done' : ''}`}>
      <div className="task-content">
        <label className="checkbox-container">
          <input 
            type="checkbox" 
            checked={task.is_done} 
            onChange={handleToggle} 
          />
          <span className="checkmark"></span>
        </label>
        <div className="task-details">
          <h4 className="task-title">{task.description}</h4>
          <div className="task-meta">
            {category && <span className="badge category-badge">{category.name}</span>}
            {isQuadValid && <span className={`badge quad-badge quad-${task.quadrant}`}>{task.quadrant}</span>}
            {task.due_date && <span className="badge date-badge">Due: {new Date(task.due_date).toLocaleDateString()}</span>}
            {task.estimated_effort_hours && <span className="badge effort-badge">{task.estimated_effort_hours}h</span>}
          </div>
        </div>
      </div>
      <button className="btn-icon delete-btn" onClick={handleDelete} title="Delete Task">
        &times;
      </button>
    </div>
  );
}
