'use client';

import React, { useState } from 'react';
import { createCategory } from '../utils/api';

interface CategorySetupProps {
  onCategoryCreated: () => void;
}

export default function CategorySetup({ onCategoryCreated }: CategorySetupProps) {
  const [name, setName] = useState('');
  const [coefficient, setCoefficient] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setLoading(true);
    try {
      await createCategory(name, coefficient);
      setName('');
      setCoefficient(1);
      onCategoryCreated();
    } catch (err: any) {
      console.error(err);
      alert(err.message || 'Failed to create category');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="category-setup glass-panel">
      <h3 className="section-title">Add Category</h3>
      <form onSubmit={handleSubmit} className="flex-col gap-4">
        <div className="form-group">
          <label>Category Name</label>
          <input 
            type="text" 
            placeholder="e.g. Work, Personal" 
            value={name} 
            onChange={e => setName(e.target.value)}
            className="form-input"
            required 
          />
        </div>
        <div className="form-group">
          <label>Weight / Coefficient</label>
          <input 
            type="number" 
            step="0.1" min="0.1"
            value={coefficient} 
            onChange={e => setCoefficient(Number(e.target.value))}
            className="form-input"
            required 
          />
        </div>
        <button type="submit" className="btn btn-secondary w-full" disabled={loading}>
          {loading ? 'Saving...' : 'Save Category'}
        </button>
      </form>
    </div>
  );
}
