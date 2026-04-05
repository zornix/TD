'use client';

import React from 'react';
import { Task, Category } from '../utils/types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  categories: Category[];
  onUpdate: () => void;
  title: string;
}

export default function TaskList({ tasks, categories, onUpdate, title }: TaskListProps) {
  if (tasks.length === 0) {
    return null; // Don't render empty lists
  }

  return (
    <div className="task-list">
      <h3 className="section-title">{title}</h3>
      <div className="task-list-container">
        {tasks.map(task => (
          <TaskItem 
            key={task.id} 
            task={task} 
            category={categories.find(c => c.id === task.category_id)}
            onUpdate={onUpdate} 
          />
        ))}
      </div>
    </div>
  );
}
