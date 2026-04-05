'use client';

import React, { useState } from 'react';
import { Category } from '../utils/types';
import { createTask } from '../utils/api';

interface TaskFormProps {
  categories: Category[];
  onTaskCreated: () => void;
}

export default function TaskForm({ categories, onTaskCreated }: TaskFormProps) {
  const [description, setDescription] = useState('');
  const [importance, setImportance] = useState(5);
  const [categoryId, setCategoryId] = useState<number | ''>('');
  const [dueDate, setDueDate] = useState('');
  const [effortHours, setEffortHours] = useState('');

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim() || categoryId === '') {
      alert('Please provide description and category.');
      return;
    }

    setLoading(true);
    try {
      await createTask({
        description,
        importance,
        category_id: Number(categoryId),
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
        estimated_effort_hours: effortHours ? Number(effortHours) : null,
      });
      
      // Reset form
      setDescription('');
      setImportance(5);
      setDueDate('');
      setEffortHours('');
      onTaskCreated();
    } catch (err: any) {
      console.error(err);
      alert(err.message || 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  if (categories.length === 0) {
    return (
      <div className="glass-panel text-center">
        <p>Please create categories first to add tasks.</p>
      </div>
    );
  }

  return (
    <form className="task-form glass-panel" onSubmit={handleSubmit}>
      <h3 className="section-title">Add New Task</h3>
      
      <div className="form-group">
        <input 
          type="text" 
          placeholder="What needs to be done?" 
          value={description} 
          onChange={(e) => setDescription(e.target.value)}
          className="form-input text-lg"
          required
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Category</label>
          <select 
            value={categoryId} 
            onChange={(e) => setCategoryId(e.target.value === '' ? '' : Number(e.target.value))}
            className="form-input"
            required
          >
            <option value="" disabled>Select category</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Importance (1-10)</label>
          <input 
            type="number" 
            min="1" max="10"
            value={importance} 
            onChange={(e) => setImportance(Number(e.target.value))}
            className="form-input"
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Due Date</label>
          <input 
            type="date" 
            value={dueDate} 
            onChange={(e) => setDueDate(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>Effort (Hours)</label>
          <input 
            type="number" 
            step="0.5" min="0"
            value={effortHours} 
            onChange={(e) => setEffortHours(e.target.value)}
            className="form-input"
          />
        </div>
      </div>

      <button type="submit" className="btn btn-primary mt-4 w-full disabled:opacity-50" disabled={loading}>
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
