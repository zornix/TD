'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { Task, Category } from '../utils/types';
import { getTasks, getCategories } from '../utils/api';
import TaskList from './TaskList';
import TaskForm from './TaskForm';
import CategorySetup from './CategorySetup';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [fetchedTasks, fetchedCategories] = await Promise.all([
        getTasks(),
        getCategories()
      ]);
      setTasks(fetchedTasks);
      setCategories(fetchedCategories);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const activeTasks = tasks.filter(t => !t.is_done);
  const doneTasks = tasks.filter(t => t.is_done);

  return (
    <div className="dashboard-layout container">
      {/* Sidebar for config and metadata */}
      <aside className="sidebar">
        <div className="app-branding">
          <div className="logo-icon">✓</div>
          <h1>TaskFlow</h1>
          <p>Prioritize your work intelligently.</p>
        </div>
        
        <CategorySetup onCategoryCreated={fetchData} />

        <div className="glass-panel stats-panel mt-6">
          <h3 className="section-title">Stats</h3>
          <ul className="stats-list">
             <li>Active Tasks: <strong>{activeTasks.length}</strong></li>
             <li>Completed: <strong>{doneTasks.length}</strong></li>
             <li>Categories: <strong>{categories.length}</strong></li>
          </ul>
        </div>
      </aside>

      {/* Main content area */}
      <main className="main-content">
        <TaskForm categories={categories} onTaskCreated={fetchData} />
        
        {loading ? (
          <div className="loader">Loading tasks...</div>
        ) : (
          <div className="tasks-container mt-6">
            <TaskList 
              title="Active Tasks" 
              tasks={activeTasks} 
              categories={categories} 
              onUpdate={fetchData} 
            />
            {doneTasks.length > 0 && (
              <TaskList 
                title="Completed Tasks" 
                tasks={doneTasks} 
                categories={categories} 
                onUpdate={fetchData} 
              />
            )}
            
            {tasks.length === 0 && (
              <div className="empty-state">
                <h2>All caught up!</h2>
                <p>Add a new task to get started.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
